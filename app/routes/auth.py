import re
from re import Pattern
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

whitelistnum = re.compile(r"^[a-zA-Z0-9]+$")
whitelist = re.compile(r"^[a-zA-Z]+$")


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
    if request.method != "POST":
        link: str | None = request.args.get("link")
        link = "" if link is None else link
        return render_template("login.html", link=link)

    usr = request.form.get("usr") or None
    pwd = request.form.get("pwd") or None

    if usr is None or pwd is None:
        flash("You haven't compiled the username or the password fields", "error")
        return render_template("login.html")

    dbUsers = db.session.scalars(sq.select(User).where(User.username == usr)).fetchall()

    if len(dbUsers) == 0:
        # TODO: merge this check with the following one (security risk, debug only)
        flash("Specified user doesn't exist", "error")
        return render_template("login.html")

    if not bcrypt.check_password_hash(dbUsers[0].password, pwd):
        flash("The password is wrong", "error")
        return render_template("login.html")

    dbUsers[0].token = (
        getNewToken()
    )  # create a new session token and save it on the database
    session["token"] = dbUsers[0].token

    db.session.commit()  # commit the new token to the db

    rlink: str | None = request.form.get("link")

    if (
        rlink is not None and rlink != ""
    ):  # if a new lin has been provided, redirect to that
        return redirect(rlink)
    else:
        flash("You have successfully logged in", "success")
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
    """
    Function used to provide the registration form to the user and
    to validate his registration requests
    """
    if request.method != "POST":  # provide the normal registration page
        return render_template("register.html", regform=RegForm())

    regform = RegForm(request.form)  # load the form from its template
    regform.validate_on_submit()

    usr = request.form.get("usr") or None
    frname = request.form.get("frname") or None
    lsname = request.form.get("frname") or None
    pwd = request.form.get("pwd") or None
    checkpwd = request.form.get("checkpwd") or None
    seller = request.form.get("seller") or ""

    if None in [usr, frname, lsname, pwd, checkpwd]:
        flash("You have to compile all the fields", "error")
        return render_template(
            "register.html",
            regform=regform,
        )

    usr = str(usr)  # prevent mypy from complaining abount None values
    frname = str(frname)
    lsname = str(lsname)
    pwd = str(pwd)
    checkpwd = str(checkpwd)

    # checking the username
    if not whitelistnum.match(usr) and len(usr) > 0:
        flash("Username can only contain letters and numbers", "error")
        return render_template(
            "register.html",
            regform=regform,
        )
    # checking the name and surname
    for field in [frname, lsname]:
        if not whitelist.match(field) and len(field) > 0:
            flash("The Name and the Surname must contain only letter", "error")
            return render_template(
                "register.html",
                regform=regform,
            )
    # checking password length and equality
    if len(pwd) < 8 or len(checkpwd) < 8:
        flash(
            f"Password/s fields must be at least {minPwdLen} characters long", "error"
        )
        return render_template(
            "register.html",
            regform=regform,
        )
    if pwd != checkpwd:
        flash("Passwords must be the same", "error")
        return render_template(
            "register.html",
            regform=regform,
        )

    # check wether the username already exists
    dbUsers = db.session.scalars(sq.select(User).where(User.username == usr)).fetchall()
    if len(dbUsers) != 0:
        flash("Username already taken", "error")
        return render_template(
            "register.html",
            regform=regform,
        )

    newUsersToken: str = getNewToken()  # generate a new session token
    db.session.add(  # save the user to the database
        User(
            usr,
            frname,
            lsname,
            str(
                bcrypt.generate_password_hash(pwd, bcryptRounds).decode("utf-8")
            ),  # generate salted password
            datetime.now(),
            datetime.now(),
            0,
            seller == "y",  # if the user has ticked the checkbox, make him a seller
            newUsersToken,
        )
    )
    session["token"] = newUsersToken  # save the token (user's side)
    db.session.commit()  # save the changes into the database

    flash("You have successfully registered", "success")
    return redirect("/")


@app.route("/logout/")
def logout() -> str | Response:
    """
    Function used to delete the session token both client and server side
    """
    loggedOut: bool = False
    if session.get("token"):  # check if the users has already been logged out
        users = db.session.scalars(  # find the user with the provided token
            sq.select(User).filter_by(token=session["token"])
        ).fetchall()
        if len(users) == 1:  # if a user is found
            users[0].token = None  # clear the token database side
            db.session.commit()
            loggedOut = True
    session.clear()  # clear the token client side
    if loggedOut:
        flash("You have beem logged out successfully", "success")
    return redirect("/")


@app.errorhandler(CSRFError)
def handle_csrf_error(e: CSRFError) -> tuple[str, int]:
    """
    If an error with the csrf token happends, be sure to display it with
    a meaningful webpage
    """
    return (
        render_template("error.html", errorName="CSRF Error", errorMsg=e.description),
        400,
    )


def getNewToken() -> str:
    """
    Helper function to generate a new token
    """
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
    if not session.get("token"):  # if the token doesn't exists
        return False
    users = db.session.scalars(  # get the user with the corresponding token
        sq.select(User).filter_by(token=session["token"])
    ).fetchall()
    if (
        len(users) != 1
        or (  # check if the token is still valid (1 day)
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
    if not session.get("token"):  # if the token doesn't exists
        return None
    users = db.session.scalars(  # get the user with the corresponding token
        sq.select(User).filter_by(token=session["token"])
    ).fetchall()
    if (
        len(users) != 1
        or (  # check if the token is still valid (1 day)
            datetime.combine(users[0].last_logged_in_at, datetime.min.time())
            - datetime.now()
        ).days
        >= 1
    ):
        return None
    return users[0]
