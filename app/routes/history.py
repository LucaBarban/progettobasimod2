from typing import Tuple
from flask import current_app as app, flash, render_template, request, redirect
import sqlalchemy as sq
from sqlalchemy import exc
from app.database import db
from app.routes.auth import getLoggedInUser #type: ignore
from werkzeug.wrappers.response import Response
from app.models.history import History
from app.models.user import User

@app.route("/history/", methods=['GET', 'POST'])
def history() -> str | Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/history")

    hid: str|None = request.form.get("hid")
    rew: str|None = request.form.get("review")

    if request.method != 'POST':
        if hid is not None and rew is not None and len(rew) >= 2:
            hsToUpd = db.session.scalars(sq.select(History).where(History.id == hid)).one()

            if hsToUpd is None:
                flash("Invalid book selectet for review")
            elif hsToUpd.recensione is not None:
                flash("You have already reviewed this book")
            else:
                hsToUpd.recensione = rew
                db.session.commit()
        else:
            flash("Be sure to give a review that has some sense")

    hsts = db.session.scalars(sq.select(History).where(History.fk_buyer == usr.username).order_by(History.id.desc())).fetchall()
    return render_template("history.html", user = usr, hsts = hsts)
