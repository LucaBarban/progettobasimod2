from collections.abc import Callable
from typing import List, TypeVar

from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.history import History, Statuses
from app.routes.auth import getLoggedInUser

T = TypeVar("T")


def partition(fn: Callable[[T], bool], items: List[T]) -> tuple[List[T], List[T]]:
    """
    Split a list into two
    `fn` returns `true` for all the items in the first list and `false` for all in the second
    """

    a = []
    b = []
    for item in items:
        if fn(item):
            a.append(item)
        else:
            b.append(item)

    return (a, b)


@app.route("/orders/<int:id>", methods=["POST"])
def update(id: int) -> Response:
    """
    Update the status for an order
    """

    user = getLoggedInUser()
    status = request.form.get("status")

    # Validate form input
    if user is None or status not in Statuses:
        flash("An error occoured", "error")
        return redirect("/")

    item = db.session.get(History, id)

    if item is None or item.seller.username != user.username:
        flash("Cannot find the right insertion", "error")
        return redirect("/")

    # Update status
    item.status = status

    db.session.commit()

    return redirect("/orders/")


@app.route("/orders/")
def orders() -> str | Response:
    """
    Display all the orders handled by a user
    """

    user = getLoggedInUser()
    if user is None:
        return redirect("/login/?link=/orders")

    # Block users that are not sellers from entering
    if user.seller == False:
        # Mabye custom page?
        abort(404)

    orders = db.session.query(History).filter(History.fk_seller == user.username).all()

    # Split orders into [ not shipped, shipped, delivered ]
    (processing, orders) = partition(
        lambda h: h.status in {"processing", "packing"}, orders
    )
    (shipping, done) = partition(lambda h: h.status != "delivered", orders)

    return render_template(
        "orders.html", user=user, processing=processing, shipping=shipping, done=done
    )
