from typing import Tuple

import sqlalchemy as sq
from flask import current_app as app
from flask import flash, redirect, render_template, request
from sqlalchemy import exc
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.own import Own
from app.models.user import User
from app.routes.auth import getLoggedInUser


@app.route("/insertion/", methods=["GET", "POST"])
def insertion() -> str | Response:
    """
    Debug function, now its here just to redirect traffic
    if its needed
    """
    return redirect("/library")
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    books = db.session.scalars(
        sq.select(Own).where(Own.fk_username == usr.username)
    ).fetchall()

    ownedbooks = []
    sellingbooks = []

    for i in range(0, len(books)):
        if books[i].price is None:
            ownedbooks.append(books[i])
        else:
            sellingbooks.append(books[i])

    return render_template(
        "intertionmanager.html", ownedbooks=ownedbooks, sellingbooks=sellingbooks
    )


@app.route("/insertion/update/", methods=["GET"])
def getInsertionUpdateForm() -> str | Response:
    """
    Provide the update form prepopulated with the exisitng values
    """
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    if not usr.seller:
        flash("Your account is not a seller account, so you can't update insertions")
        return redirect("/library")
    book: str | None = request.args.get("book")
    bookstate: str | None = request.args.get("bookstate")
    quantity: str | None = request.args.get("quantity")
    oldprice: str | None = request.args.get("oldprice")
    if book is None or bookstate is None or quantity is None or oldprice is None:
        return redirect(
            "/insertion"
        )  # if some parameters are missing return the insertion page
    return render_template(
        "updateinsertion.html",
        user=usr,
        book=book,
        bookstate=bookstate,
        quantity=quantity,
        oldprice=int(oldprice) / 100,
    )


@app.route("/insertion/list/", methods=["GET"])
def getInsertionListForm() -> str | Response:
    """
    Provide the list form
    """
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    if not usr.seller:
        flash("Your account is not a seller account, so you can't list books for sale")
        return redirect("/library")
    book: str | None = request.args.get("book")
    bookstate: str | None = request.args.get("bookstate")
    if book is None or bookstate is None:
        return redirect(
            "/insertion"
        )  # if some parameters are missing return the insertion page
    return render_template(
        "listinsertion.html", user=usr, book=book, bookstate=bookstate
    )


@app.route("/insertion/unlist/", methods=["GET"])
def getInsertionUnListForm() -> str | Response:
    """Provide the unlisting form"""
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    if not usr.seller:
        flash("Your account is not a seller account, so you can't unlist an insertion")
        return redirect("/library")
    book: str | None = request.args.get("book")
    bookstate: str | None = request.args.get("bookstate")
    price: str | None = request.args.get("price")
    quantity: str | None = request.args.get("quantity")
    if None in [book, bookstate, price, quantity]:
        return redirect(
            "/insertion"
        )  # if some parameters are missing return the insertion page
    price = str(price)  # prevent mypy from complaining
    return render_template(
        "unlistinsertion.html",
        user=usr,
        book=book,
        bookstate=bookstate,
        price=int(price) / 100,
        quantity=quantity,
    )


@app.route("/insertion/update/", methods=["POST"])
def updatebook() -> str | Response:
    """
    Once all the updated information are provided, update the corresponding
    insertion on the database
    """
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    if not usr.seller:
        flash("Your account is not a seller account, so you can't update an insertion")
        return redirect("/library")

    (oldPriceBooks, newPriceBooks, quantity, oldprice, newprice) = retriveExistingBooks(
        usr
    )  # get the currently existing insertions and books
    if quantity is None or oldprice is None:
        flash(
            "Missing parameters, be sure to compile them (if the new price is not compiled, "
            + "the operation will be threated like an insertion removal)",
            "error",
        )
        return redirect("/insertion")

    if oldPriceBooks is None:
        flash("You don't own the selected book or it's not being sold", "error")
        return redirect("/insertion")

    if quantity <= 0:
        flash("Invalid quantity", "error")
        return redirect("/insertion")

    if newprice is None:  # if the price is None, remove the book
        insState: Tuple[str, bool] = manageInsertion(
            usr, newPriceBooks, oldPriceBooks, quantity, oldprice, False
        )
        if not insState[1]:
            flash(
                "An error occured during insertion's deletion/update: " + insState[0],
                "error",
            )
            return redirect("/insertion")
    else:
        try:
            # if an insertion with the same price already exists
            if newPriceBooks is not None:
                newPriceBooks.quantity += quantity  # add the new quantity
            else:
                db.session.add(  # create a new insertion if there wasn't an existing one
                    Own(
                        usr.username,
                        oldPriceBooks.fk_book,
                        oldPriceBooks.state,
                        newprice,
                        quantity,
                    )
                )
            db.session.delete(oldPriceBooks)
        except exc.SQLAlchemyError:
            db.session.rollback()
            flash(
                "An unexpected error occured while interacting with the database",
                "error",
            )
            return redirect("/insertion")

    db.session.commit()
    return redirect("/insertion")


@app.route("/insertion/list/", methods=["POST"])
def listbook() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    if not usr.seller:
        flash("Your account is not a seller account, so you can't list an insertion")
        return redirect("/library")

    (ownedBook, ownedBookOnSale, quantity, price) = retriveBooks(
        usr
    )  # get the books owned by the user (including the ones that are being sold)
    if quantity is None or price is None:
        flash("Missing parameters, be sure to compile them all", "error")
        return redirect("/insertion")

    if ownedBook is None:
        flash("You don't own the selected book", "error")
        return redirect("/insertion")

    if (
        ownedBook.quantity < quantity or quantity <= 0
    ):  # check if the quantity is right and sufficient
        flash(
            f"You dont have enough books to sell ('{quantity}' when {ownedBook.quantity} are avaiable )",
            "error",
        )
        return redirect("/insertion")

    insState: Tuple[str, bool] = manageInsertion(
        usr, ownedBook, ownedBookOnSale, quantity, price, True
    )  # try to add the insertion
    if not insState[1]:
        flash(
            "An error occured during insertion's creation/update: " + insState[0],
            "error",
        )
        return redirect("/insertion")

    return redirect("/insertion")


@app.route("/insertion/unlist/", methods=["POST"])
def unlistbook() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    if not usr.seller:
        flash("Your account is not a seller account, so you can't unlist an insertion")
        return redirect("/library")

    (ownedBook, ownedBookOnSale, quantity, price) = retriveBooks(
        usr
    )  # get the currently existing insertions and books
    if quantity is None or price is None:
        flash("Missing parameters, be sure to compile them all", "error")
        return redirect("/insertion")

    if ownedBookOnSale is None:
        flash("You aren't selling the selected book", "error")
        return redirect("/insertion")

    if (
        ownedBookOnSale.quantity < quantity or quantity <= 0
    ):  # check if the quantity is right and sufficient
        flash(
            f"You dont have enough books to unlist ('{quantity}' when {ownedBookOnSale.quantity} are avaiable )"
        )
        return redirect("/insertion")

    insState: Tuple[str, bool] = manageInsertion(
        usr, ownedBook, ownedBookOnSale, quantity, price, False
    )  # try to remove the insertion
    if not insState[1]:
        flash(
            f"An error occured during insertion's deletion/update: {insState[0]}",
            "error",
        )
        return redirect("/insertion")

    return redirect("/insertion")


def retriveBooks(usr: User) -> tuple[Own | None, Own | None, int | None, int | None]:
    """
    Returns the books owned by the user divided in not selling and selling ones,
    the quantity requested by the user and the specified price
    """
    book: str | None = request.form.get("book") or None
    bookstate: str | None = request.form.get("bookstate") or None
    quantity: int | None = request.form.get("quantity", type=int) or None
    fprice: float | None = request.form.get("price", type=float)
    price: int | None = int(fprice * 100) if fprice else None

    if book is None or bookstate is None or quantity is None or price is None:
        return (None, None, None, None)  # if not all the parameters are populated

    ownedBook: Own | None = db.session.scalar(  # books that are not being sold
        sq.select(Own)
        .where(Own.fk_username == usr.username)
        .where(Own.fk_book == book)
        .where(Own.state == bookstate)
        .where(Own.price == None)
    )
    ownedBookOnSale: Own | None = db.session.scalar(  # books that are being sold
        sq.select(Own)
        .where(Own.fk_username == usr.username)
        .where(Own.fk_book == book)
        .where(Own.state == bookstate)
        .where(Own.price == price)
    )
    return (ownedBook, ownedBookOnSale, quantity, price)


def retriveExistingBooks(
    usr: User,
) -> tuple[Own | None, Own | None, int | None, int | None, int | None]:
    """
    Returns the books owned by the user divided in not selling and selling ones,
    the quantity requested by the user and the specified old and new prices
    """
    book: str | None = request.form.get("book") or None
    bookstate: str | None = request.form.get("bookstate") or None
    quantity: int | None = request.form.get("quantity", type=int) or None
    foldprice: float | None = request.form.get("oldprice", type=float)
    oldprice: int | None = int(foldprice * 100) if foldprice else None
    fnewprice: float | None = request.form.get("newprice", type=float) or None
    newprice: int | None = int(fnewprice * 100) if fnewprice else None

    if book is None or bookstate is None or quantity is None or oldprice is None:
        return (None, None, None, None, None)

    oldPriceBooks: Own | None = db.session.scalar(  # books with old price
        sq.select(Own)
        .where(Own.fk_username == usr.username)
        .where(Own.fk_book == book)
        .where(Own.state == bookstate)
        .where(Own.price == oldprice)
    )
    newPriceBooks: Own | None = db.session.scalar(  # books with new price
        sq.select(Own)
        .where(Own.fk_username == usr.username)
        .where(Own.fk_book == book)
        .where(Own.state == bookstate)
        .where(Own.price == newprice)
    )
    return (oldPriceBooks, newPriceBooks, quantity, oldprice, newprice)


def manageInsertion(
    usr: User,
    ownedBook: Own | None,
    ownedBookOnSale: Own | None,
    quantity: int,
    price: int | None,
    add: bool,
) -> Tuple[str, bool]:
    """
    This funtion manages the insertions.
    If add is positive, it will expext 'ownedBook' to be not None and it will
    create/update the insertions and/or delete the books that are not being sold as necessary.
    If add is negative, it will expect `ownedBookOnSale` to be not None and it will
    create/update the user's books that where being sold and/or delete the inserions.
    """
    if quantity <= 0:
        return ("Requested quantity is less or eqaul to 0, doing nothing", False)
    if price is None:
        return ("A price was not guven to the function", False)

    opreatinMsg: str
    try:
        if add and ownedBook is not None:  # creates/updates an insertion
            if ownedBook.quantity == quantity:  # if all the books have to be sold
                if ownedBookOnSale is not None:  # if an insertion already exists
                    ownedBookOnSale.quantity += quantity
                    opreatinMsg = f"Existing insertion has been updated with {{{quantity}}} more books, none remaining"
                else:
                    db.session.add(  # create a new insertion
                        Own(
                            usr.username,
                            ownedBook.fk_book,
                            ownedBook.state,
                            price,
                            quantity,
                        )
                    )
                    opreatinMsg = f"New insertion has been created with {{{quantity}}} books, none remaining"
                db.session.delete(ownedBook)  # delete books that are't being sold
            else:  # if some books won't be sold
                if ownedBookOnSale is not None:  # if an insertion already exists
                    ownedBookOnSale.quantity += quantity
                    opreatinMsg = f"Existing insertion has been updated with {{{quantity}}} more books, some remain to sell"
                else:
                    db.session.add(  # create a new insertion
                        Own(
                            usr.username,
                            ownedBook.fk_book,
                            ownedBook.state,
                            price,
                            quantity,
                        )
                    )
                    opreatinMsg = f"New insertion has been created with {{{quantity}}} books, some remain to sell"
                ownedBook.quantity -= quantity  # remove books that were not being sold
        elif not add and ownedBookOnSale is not None:  # deletes/updates an insertion
            if ownedBookOnSale.quantity == quantity:  # if all books won't be on sale
                if ownedBook is not None:  # if books not on sale exist
                    ownedBook.quantity += quantity
                    opreatinMsg = f"Insertion has been deleted, {{{quantity}}} existing books added to library"
                else:
                    db.session.add(  # create record for books not on sale
                        Own(
                            usr.username,
                            ownedBookOnSale.fk_book,
                            ownedBookOnSale.state,
                            None,
                            quantity,
                        )
                    )
                    opreatinMsg = f"Insertion has been deleted, {{{quantity}}} new books added to library"
                db.session.delete(ownedBookOnSale)  # remove all books on sale

            else:  # if some books won't be removed
                if ownedBook is not None:  # if books not on sale exist
                    ownedBook.quantity += quantity
                    opreatinMsg = f"{{{quantity}}} existing books moved to the library, some remain listed"
                else:
                    db.session.add(  # create record for books not on sale
                        Own(
                            usr.username,
                            ownedBookOnSale.fk_book,
                            ownedBookOnSale.state,
                            None,
                            quantity,
                        )
                    )
                    opreatinMsg = f"{{{quantity}}} new books moved to the library, some remain listed"
                ownedBookOnSale.quantity -= quantity  # remove books that are being sold
        else:
            db.session.rollback()
            return "Invalid state of owned/insertioned books passed to function", False
    except exc.SQLAlchemyError:
        db.session.rollback()
        return "An unexpected error occured while interacting with the database", False

    db.session.commit()
    return (opreatinMsg, True)
