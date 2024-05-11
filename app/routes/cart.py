from datetime import datetime

import sqlalchemy as sq
from flask import current_app as app
from flask import redirect, render_template, request
from psycopg2.errors import CheckViolation, RaiseException
from sqlalchemy import exc
from typing_extensions import Tuple

from app.database import db
from app.models.cart import Cart
from app.models.history import History
from app.models.own import Own
from app.models.user import User
from app.routes.auth import getLoggedInUser

OwnIndex = Tuple[str, str, str, str]


def cart_get(user: User, err: str | None = None) -> str:
    items = db.session.scalars(
        sq.select(Cart).filter(Cart.fk_buyer == user.username)
    ).all()

    availables = [item.own.quantity for item in items]

    total = sum([item.own.price * item.quantity for item in items])

    return render_template(
        "cart.html",
        items=items,
        availables=availables,
        user=user,
        total=total,
        error=err,
    )


def add_history(own: Own, user: User, quantity: int):
    db.session.add(
        History(
            date=datetime.now(),
            quantity=quantity,
            status="shipped",
            price=own.price,
            fk_buyer=user.username,
            fk_seller=own.fk_username,
            fk_book=own.fk_book,
            state=own.state,
        )
    )


def cart_post(user: User) -> str:
    own_ids = request.form.getlist("own")
    quantities = request.form.getlist("quantity")
    quantities = [int(q) for q in quantities]

    price_total = 0

    try:
        for i, own_id in enumerate(own_ids):
            own = db.session.get_one(Own, own_id)

            add_history(own, user, quantities[i])

            own.quantity -= quantities[i]
            price_total += own.price * quantities[i]

        user.balance -= price_total

        db.session.query(Cart).filter(Cart.fk_buyer == user.username).delete()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        err = e.__dict__["orig"]
        print(err)
        if type(err) == RaiseException:
            return cart_get(
                user, "Some insertions have been removed or their quantity decreased"
            )
        elif type(err) == CheckViolation:
            return cart_get(user, "Not enough money on account")
        else:
            return cart_get(user, "An error occoured")

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
