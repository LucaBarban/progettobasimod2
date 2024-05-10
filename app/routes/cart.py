import sqlalchemy as sq
from flask import current_app as app
from flask import redirect, render_template, request
from sqlalchemy import exc
from typing_extensions import Tuple

from app.database import db
from app.models.cart import Cart
from app.models.own import Own
from app.models.user import User
from app.routes.auth import getLoggedInUser

OwnIndex = Tuple[str, str, str, str]


def cart_get(user: User) -> str:
    items = db.session.scalars(
        sq.select(Cart).filter(Cart.fk_buyer == user.username)
    ).all()

    total = sum([item.own.price * item.quantity for item in items])

    return render_template("cart.html", items=items, user=user, total=total)


def cart_post(user: User) -> str:
    own_ids = request.form.getlist("own")
    quantities = request.form.getlist("quantity")
    quantities = [int(q) for q in quantities]

    price_total = 0

    try:
        for i, own_id in enumerate(own_ids):
            own = db.session.get_one(Own, own_id)
            own.quantity -= quantities[i]
            price_total += own.price * quantities[i]

        user.balance -= price_total

        db.session.query(Cart).filter(Cart.fk_buyer == user.username).delete()
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return "<h1> AN ERROR OCCOURED </h1>"

    return "<h1>All Good</h1>"


@app.route("/cart/", methods=["GET", "POST"])
def cart() -> str:
    user = getLoggedInUser()
    if user is None:
        return redirect("/login")

    if request.method == "GET":
        return cart_get(user)
    else:
        return cart_post(user)
