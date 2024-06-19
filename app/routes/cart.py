from datetime import datetime

import sqlalchemy as sq
from flask import current_app as app
from flask import flash, redirect, render_template, request
from psycopg2.errors import CheckViolation, RaiseException
from sqlalchemy import exc
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.cart import Cart
from app.models.history import History
from app.models.own import Own
from app.models.user import User
from app.routes.auth import getLoggedInUser


def cart_get(user: User, err: str | None = None) -> str:
    items = db.session.scalars(
        sq.select(Cart).filter(Cart.fk_buyer == user.username)
    ).all()

    total = sum([item.own.price * item.quantity for item in items])  # type: ignore

    if err is not None:
        flash(err, "error")

    return render_template(
        "cart.html",
        items=items,
        user=user,
        total=total,
    )


def add_history(own: Own, user: User, quantity: int) -> None:
    db.session.add(
        History(
            date=datetime.now(),
            quantity=quantity,
            status="processing",
            price=own.price,
            fk_buyer=user.username,
            fk_seller=own.fk_username,
            fk_book=own.fk_book,
            state=own.state,
        )
    )


def add_library(own: Own, user: User, quantity: int) -> None:
    insertion = (
        db.session.query(Own)
        .filter(
            Own.fk_username == user.username,
            Own.fk_book == own.fk_book,
            Own.state == own.state,
            Own.price == -1,
        )
        .one_or_none()
    )

    if insertion is not None:
        insertion.quantity += quantity
    else:
        db.session.add(
            Own(
                fk_username=user.username,
                fk_book=own.fk_book,
                state=own.state,
                quantity=quantity,
                price=None,
            )
        )

    db.session.commit()


def cart_post(user: User) -> str | Response:
    own_ids = request.form.getlist("own")

    price_total = 0

    try:
        for own_id in own_ids:
            own = db.session.get_one(Own, own_id)

            if own.price is None:
                raise ValueError("Cannot buy a book not on sale")

            quantity_str = request.form.get(f"quantity-{own.id}")
            if quantity_str is None:
                raise ValueError("Missing item quantity")

            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            add_history(own, user, quantity)
            add_library(own, user, quantity)

            own.quantity -= quantity
            own.user.balance += own.price * quantity
            price_total += own.price * quantity

        user.balance -= price_total

        db.session.query(Cart).filter(Cart.fk_buyer == user.username).delete()
        db.session.commit()

    except exc.NoResultFound:
        db.session.rollback()
        return cart_get(
            user,
            "The status of some insertion has changed, the page has been refreshed",
        )

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        err = e.__dict__["orig"]

        if type(err) == RaiseException:
            return cart_get(
                user, "Some insertions have been removed or their quantity decreased"
            )
        elif type(err) == CheckViolation:
            return cart_get(user, "Not enough money on account")
        else:
            return cart_get(user, "An error occoured")

    except:
        db.session.rollback()
        return cart_get(user, "An error occoured")

    flash("Your order has been confirmed", "success")
    return redirect("/history")


@app.route("/cart/", methods=["GET", "POST"])
def cart() -> str | Response:
    user = getLoggedInUser()
    if user is None:
        return redirect("/login")

    if request.method == "GET":
        return cart_get(user)
    else:
        return cart_post(user)


@app.route("/cart/add/<int:id>", methods=["POST"])
def cart_add(id: int) -> Response:
    user = getLoggedInUser()

    quantity = request.form.get("quantity")

    insertion = db.session.get(Own, id)

    if insertion is None:
        flash("An error occoured", "error")
        return redirect("/")
    elif quantity is None or int(quantity) <= 0:
        flash("Wrong value for quantity", "error")
        return redirect(f"/book/{insertion.book.id}")
    elif int(quantity) > insertion.quantity:
        flash("Maximum quantity exceeded", "error")
        return redirect(f"/book/{insertion.book.id}")
    elif user is None:
        flash("User not logged in", "error")
        return redirect(f"/book/{insertion.book.id}")

    cart = (
        db.session.query(Cart)
        .filter(Cart.fk_buyer == user.username, Cart.fk_own == id)
        .one_or_none()
    )

    if cart is None:
        db.session.add(Cart(fk_buyer=user.username, fk_own=id, quantity=quantity))
    else:
        cart.quantity += int(quantity)

    try:
        db.session.commit()
    except:
        flash("An error occoured", "error")
        db.session.rollback()

    return redirect(f"/book/{insertion.book.id}")


@app.route("/cart/remove/<int:id>")
def cart_remove(id: int) -> Response:
    user = getLoggedInUser()
    if user is None:
        return redirect("/login")

    try:
        item = (
            db.session.query(Cart)
            .join(Cart.own)
            .filter(Cart.fk_buyer == user.username, Own.id == id)
            .one()
        )

        db.session.query(Cart).filter(
            Cart.own == item.own, Cart.fk_buyer == item.fk_buyer
        ).delete()

        db.session.commit()
    except:
        db.session.rollback()

    return redirect("/cart")
