from flask import current_app as app
from flask import flash, redirect, render_template, request
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.user import User
from app.routes.auth import getLoggedInUser, bcryptRounds, minPwdLen, whitelist

from ..safety import bcrypt


@app.route("/profile/", methods=["GET", "POST"])
def profile() -> str | Response:
    """
    Provide and process the user's information update form
    """
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/profile/")

    if request.method != "POST":
        return render_template("profile.html", user=usr)

    err: bool = False

    frname: str | None = request.form.get("frname")  # get all the data
    lsname: str | None = request.form.get("lsname")
    pwd: str | None = request.form.get("pwd")
    rpwd: str | None = request.form.get("rpwd")
    balance: str | None = request.form.get("balance")
    seller: str | None = request.form.get("seller")

    if (
        pwd is not None and rpwd is not None and len(pwd) > 0 and len(rpwd) > 0
    ):  # check the password's presence and correctness
        if pwd != rpwd or len(pwd) < minPwdLen:
            err = True
            flash(
                f"Password fields must be the same and at least {minPwdLen} characters long",
                "error",
            )
        else:  # save the new salted and hashed password
            pwd = str(bcrypt.generate_password_hash(pwd, bcryptRounds).decode("utf-8"))
    elif (pwd is None or (pwd is not None and len(pwd) == 0)) and (
        pwd is None or (rpwd is not None and len(rpwd) == 0)
    ):  # if the fields are None or empty keep the current password
        pwd = usr.password
    else:
        err = True
        flash("Both password fields must be compiled to change the password", "error")

    # if the name has not changed, keep the old one
    frname = str(frname if frname is not None else usr.first_name)
    lsname = str(lsname if lsname is not None else usr.last_name)

    if (  # check if the name is a valid one
        len(frname) == 0
        or len(lsname) == 0
        or not whitelist.match(str(frname))
        or not whitelist.match(str(lsname))
    ):
        err = True
        flash(
            "You must have a name with at least a character (so, no numbers, symbols...)",
            "error",
        )

    try:
        if balance is not None and float(balance) < 0:  # check the new balance
            err = True
            flash("The balance must be positive", "error")
    except:
        err = True
        flash("The balance must be a number", "error")

    if seller is not None and seller != "on":
        flash("You cannot downgrade your account's status")
        seller = "off"  # prevent the user from removing his seller's status
    elif seller is None:
        seller = "off"

    if not err:
        usr.first_name = frname
        usr.last_name = lsname
        usr.password = pwd  # type:ignore
        usr.balance = int(float(balance) * 100) if balance is not None else usr.balance
        usr.seller = usr.seller or seller == "on"
        db.session.commit()

    return render_template("profile.html", user=usr)
