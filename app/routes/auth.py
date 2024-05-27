import secrets
from datetime import datetime

import sqlalchemy as sq
from flask import current_app as app
from flask import flash, redirect, render_template, request, session
from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.csrf import CSRFError  # type: ignore
from werkzeug.wrappers.response import Response
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from app.database import db
from app.models.user import User

from ..safety import bcrypt, csrf

minPwdLen: int = 8
bcryptRounds: int = 10
tokenSize: int = 32


@app.route("/login/", methods=["GET", "POST"])
def login() -> str | Response:
    """
    If a GET request is made, the login form will be returned. Via a get request,
    a link can also be passed to redirect automatically the user to another page.
    The function will also parse and check the parameters passed via a POST
    request to actually log in the user (this should only be done via the
    login form)

    Example:
        return redirect("/login?link=/mylink")
    """
    if request.method == "GET":
        link: str | None = request.args.get("link")
        link = "" if link is None else link
        return render_template("login.html", error="", link=link)

    usr = request.form.get("usr") or None
    pwd = request.form.get("pwd") or None

    if usr is None or pwd is None:
        return render_template(
            "login.html",
            error="You haven't compiled the username or the password fields",
        )

    dbUsers = db.session.scalars(sq.select(User).where(User.username == usr)).fetchall()

    if len(dbUsers) == 0:
        # TODO: merge this check with the following one (security risk, debug only)
        return render_template("login.html", error="I can't find you...")

    if not bcrypt.check_password_hash(dbUsers[0].password, pwd):
        return render_template("login.html", error="Wrong guess afaik")

    dbUsers[0].token = getNewToken()
    session["token"] = dbUsers[0].token

    db.session.commit()

    rlink: str | None = request.form.get("link")

    if rlink is not None and rlink != "":
        return redirect(rlink)
    else:
        flash("You have successfully logged in")
        return redirect("/")


class RegForm(FlaskForm):  # type: ignore
    usr = StringField("Username", validators=[InputRequired()])
    frname = StringField("First Name", validators=[InputRequired()])
    lsname = StringField("Last Name", validators=[InputRequired()])
    pwd = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=minPwdLen,
                message=f"Password must be at least {minPwdLen} characters",
            ),
        ],
    )
    checkpwd = PasswordField("Repeat Password", validators=[InputRequired()])
    seller = BooleanField("Seller Account")
    sub = SubmitField("Register")


@app.route("/register/", methods=["GET", "POST"])
def register() -> str | Response:
    if request.method == "GET":
        return render_template("register.html", regform=RegForm(), error="")

    regform = RegForm(request.form)
    regform.validate_on_submit()

    usr = request.form.get("usr") or None
    frname = request.form.get("frname") or None
    lsname = request.form.get("frname") or None
    pwd = request.form.get("pwd") or None
    checkpwd = request.form.get("checkpwd") or None
    seller = request.form.get("seller") or None

    if None in [usr, frname, lsname, pwd, checkpwd, seller]:
        return render_template(
            "register.html",
            regform=regform,
            error="You have to compile all the fields",
        )

    whitelistnum = ["^a-zA-Z0-9"]
    whitelist = ["^a-zA-Z"]

    usr = str(usr)  # prevent mypy from complaining
    frname = str(frname)
    lsname = str(lsname)
    pwd = str(pwd)
    checkpwd = str(checkpwd)

    if not any(c not in whitelistnum for c in usr) and len(usr) > 0:
        return render_template(
            "register.html",
            regform=regform,
            error="Username can only contain letters and numbers",
        )
    for field in [frname, lsname]:
        if not any(c not in whitelist for c in str(field)) and len(field) > 0:
            return render_template(
                "register.html",
                regform=regform,
                error="The Name and the Surname must contain only letter",
            )

    if len(pwd) < 8 or len(checkpwd) < 8:
        return render_template(
            "register.html",
            error=f"Password/s fields must be at least {minPwdLen} characters long",
        )
    if pwd != checkpwd:
        return render_template("register.html", error="Passwords must be the same")

    dbUsers = db.session.scalars(sq.select(User).where(User.username == usr)).fetchall()
    if len(dbUsers) != 0:
        return render_template("register.html", error="Username already taken")

    newUsersToken: str = getNewToken()
    db.session.add(
        User(
            usr,
            frname,
            lsname,
            str(bcrypt.generate_password_hash(pwd, bcryptRounds).decode("utf-8")),
            datetime.now(),
            datetime.now(),
            0,
            True if seller == "y" else False,
            newUsersToken,
        )
    )
    session["token"] = newUsersToken
    db.session.commit()

    flash("You have successfully registered")
    return redirect("/")


@app.route("/logout/")
def logout() -> str | Response:
    loggedOut: bool = False
    if session.get("token"):
        users = db.session.scalars(
            sq.select(User).filter_by(token=session["token"])
        ).fetchall()
        if len(users) == 1:
            users[0].token = None
            db.session.commit()
            loggedOut = True
    session.clear()
    if loggedOut:
        flash("You have beem logged out successfully")
    return redirect("/")


@app.errorhandler(CSRFError)
def handle_csrf_error(e: CSRFError) -> tuple[str, int]:
    return (
        render_template("error.html", errorName="CSRF Error", errorMsg=e.description),
        400,
    )


def getNewToken() -> str:
    return "{" + secrets.token_hex(tokenSize) + "}"


def checkLoggedIn() -> bool:
    """
    Check if the user has logged in properly (has correct and valid session)

    Returns::
        bool: True if the user is logged in with a valid session, False otherwise

    Example::

        from app.routes.auth import checkLoggedIn #type: ignore
        from werkzeug.wrappers.response import Response
        if not checkLoggedIn():
            return redirect("/login/")
        else:
            return render_template("index.html")
    """
    if not session.get("token"):  # if a token already exists
        return False
    users = db.session.scalars(
        sq.select(User).filter_by(token=session["token"])
    ).fetchall()
    if (
        len(users) != 1
        or (
            datetime.combine(users[0].last_logged_in_at, datetime.min.time())
            - datetime.now()
        ).days
        >= 1
    ):
        return False
    return True


def getLoggedInUser() -> User | None:
    """
    Get the username of the currently logged in user

    Returns::
        str: username of the logged in user if the session is valid, None otherwise

    Example::

        from app.routes.auth import getLoggedInUser #type: ignore
        from werkzeug.wrappers.response import Response
        usr: str|None = getLoggedInUser()
        if usr is None:
            return redirect("/login/")
        else:
            return render_template("index.html")

    """
    if not session.get("token"):  # if a token already exists
        return None
    users = db.session.scalars(
        sq.select(User).filter_by(token=session["token"])
    ).fetchall()
    if (
        len(users) != 1
        or (
            datetime.combine(users[0].last_logged_in_at, datetime.min.time())
            - datetime.now()
        ).days
        >= 1
    ):
        return None
    return users[0]
