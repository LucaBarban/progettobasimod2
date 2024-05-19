from collections.abc import Callable
from typing import List, TypeVar

from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.history import History
from app.routes.auth import getLoggedInUser

T = TypeVar("T")

statuses = {"processing", "packing", "shipped", "on delivery", "delivered"}


def partition(fn: Callable[[T], bool], items: List[T]) -> tuple[List[T], List[T]]:
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
    user = getLoggedInUser()
    status = request.form.get("status")

    if user is None or status not in statuses:
        flash("An error occoured")
        return redirect("/")

    item = db.session.get(History, id)

    if item is None or item.seller.username != user.username:
        flash("Cannot find the right insertion")
        return redirect("/")

    item.status = status

    db.session.commit()

    return redirect("/orders/")


@app.route("/orders/")
def orders() -> str | Response:
    user = getLoggedInUser()
    if user is None:
        return redirect("/login/?link=/orders")

    print(user)

    if user.seller == False:
        # Mabye custom page?
        abort(404)

    orders = db.session.query(History).filter(History.fk_seller == user.username).all()

    (processing, orders) = partition(
        lambda h: h.status in {"processing", "packing"}, orders
    )
    (shipping, done) = partition(lambda h: h.status != "delivered", orders)

    return render_template(
        "orders.html", user=user, processing=processing, shipping=shipping, done=done
    )
