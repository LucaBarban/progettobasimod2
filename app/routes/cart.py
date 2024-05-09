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
    users = request.form.getlist("user")
    books = request.form.getlist("book")
    states = request.form.getlist("state")
    prices = request.form.getlist("price")
    quantities = request.form.getlist("quantity")
    quantities = [int(q) for q in quantities]

    owns_str = list(zip(users, books, states, prices))
    price_total = sum(
        [int(own[3]) * quantity for (own, quantity) in zip(owns_str, quantities)]
    )

    try:
        user.balance -= price_total

        for i, own_str in enumerate(owns_str):
            own = db.session.get_one(Own, own_str)
            own.quantity -= quantities[i]

        db.session.query(Cart).filter(Cart.fk_buyer == user.username).delete()
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return "<h1> KASJDHAKJSDASDH </h1>"

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
