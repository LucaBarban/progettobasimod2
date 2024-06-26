import sqlalchemy as sq
from flask import current_app as app
from flask import flash, redirect, render_template, request
from sqlalchemy import exc
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.history import History
from app.models.user import User
from app.routes.auth import getLoggedInUser


@app.route("/history/", methods=["GET", "POST"])
def history() -> str | Response:
    """
    Print the books the user has purchased provide a way to post a review
    with relative stars to accompany it
    """
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/history")

    if request.method == "POST":
        hid: str | None = request.form.get("hid")
        rew: str | None = request.form.get("review" + hid if hid is not None else "-1")
        rating: str | None = request.form.get(
            "rating" + hid if hid is not None else "-1"
        )

        if hid is not None and rew is not None and rating is not None and len(rew) >= 2:
            try:
                hsToUpd = db.session.scalars(  # get the book/s ordered by the user to write his experience
                    sq.select(History).where(History.id == hid)
                ).one()

                if hsToUpd is None:
                    flash("Invalid book selectet for review", "error")
                elif hsToUpd.review is not None:
                    flash("You have already reviewed this book", "error")
                else:
                    hsToUpd.review = rew  # apply the provided review and stars
                    hsToUpd.stars = max(1, min(5, int(rating)))
                    db.session.commit()
            except exc.SQLAlchemyError:
                db.session.rollback()
                # explicit rollback (users reviews are one of the most delicate parts of the project)
                flash(
                    "An unexpected error occured while interacting with the database",
                    "error",
                )
            except Exception:
                db.session.rollback()
                flash("An unexpected error occured", "error")
        else:
            flash("Be sure to give a rating and a review", "error")

    hsts = db.session.scalars(
        sq.select(History)
        .where(History.fk_buyer == usr.username)
        .order_by(History.id.desc())
    ).fetchall()  # load all purchases (including any updated ones)
    return render_template("history.html", user=usr, hsts=hsts)
