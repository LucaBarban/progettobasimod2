from typing import Tuple
from flask import current_app as app, flash, render_template, request, redirect
import sqlalchemy as sq
from sqlalchemy import exc
from app.database import db
from app.routes.auth import getLoggedInUser #type: ignore
from werkzeug.wrappers.response import Response
from app.models.own import Own
from app.models.user import User

@app.route("/insertion", methods=['GET', 'POST'])
def insertion() -> str | Response:
    return redirect("/library")
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    books = db.session.scalars(sq.select(Own).where(Own.fk_username == usr.username)).fetchall()

    ownedbooks = []
    sellingbooks = []

    for i in range(0, len(books)):
        if books[i].price is None:
            ownedbooks.append(books[i])
        else:
            sellingbooks.append(books[i])

    return render_template("intertionmanager.html", ownedbooks = ownedbooks, sellingbooks = sellingbooks)

@app.route("/insertion/update/", methods=['GET'])
def getInsertionUpdateForm() -> str | Response:
    usr : User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    book:str|None = request.args.get("book")
    bookstate:str|None = request.args.get("bookstate")
    quantity:str|None = request.args.get("quantity")
    oldprice:str|None = request.args.get("oldprice")
    if book is None or bookstate is None or quantity is None or oldprice is None:
        return redirect("/insertion")
    return render_template("updateinsertion.html", user = usr, book = book, bookstate = bookstate, quantity = quantity, oldprice = oldprice)

@app.route("/insertion/list/", methods=['GET'])
def getInsertionListForm() -> str | Response:
    usr : User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    book:str|None = request.args.get("book")
    bookstate:str|None = request.args.get("bookstate")
    if book is None or bookstate is None:
        return redirect("/insertion")
    return render_template("listinsertion.html", user = usr, book = book, bookstate = bookstate)

@app.route("/insertion/unlist/", methods=['GET'])
def getInsertionUnListForm() -> str | Response:
    usr : User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")
    book:str|None = request.args.get("book")
    bookstate:str|None = request.args.get("bookstate")
    if book is None or bookstate is None:
        return redirect("/insertion")
    return render_template("unlistinsertion.html", user = usr, book = book, bookstate = bookstate)


@app.route("/insertion/update/", methods=['POST'])
def updatebook() -> str | Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    (oldPriceBooks, newPriceBooks, quantity, oldprice, newprice) = retriveExistingBooks(usr)
    if (quantity is None or oldprice is None):
        flash("Missing parameters, be sure to compile them (if the new price is not compiled, " +
              "the operation will be threated like an insertion removal)")
        return redirect("/insertion")

    if oldPriceBooks is None:
        flash("You don't own the selected book or it's not being sold")
        return redirect("/insertion")

    if quantity <= 0:
        flash("Invalid quantity")
        return redirect("/insertion")

    if newprice is None:
        insState: Tuple[str, bool] = manageInsertion(usr, newPriceBooks, oldPriceBooks, quantity, oldprice, False)
        if not insState[1]:
            flash("An error occured during insertion's deletion/update: " + insState[0])
            return redirect("/insertion")
    else:
        try:
            if newPriceBooks is not None: # if an insertion with the same price exists already
                newPriceBooks.quantity += quantity
            else:
                db.session.add(Own(
                            usr.username,
                            oldPriceBooks.fk_book,
                            oldPriceBooks.state,
                            newprice,
                            quantity
                        ))
            db.session.delete(oldPriceBooks)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            flash("An unexpected error occured while interacting with the database")
            return redirect("/insertion")

    db.session.commit()
    return redirect("/insertion")


@app.route("/insertion/list/", methods=['POST'])
def listbook() -> str | Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    (ownedBook, ownedBookOnSale, quantity, price) = retriveBooks(usr)
    if (quantity is None or price is None):
        flash("Missing parameters, be sure to compile them all")
        return redirect("/insertion")

    if ownedBook is None:
        flash("You don't own the selected book")
        return redirect("/insertion")

    if ownedBook.quantity < quantity or quantity <= 0:
        flash("You dont have enough books to sell ('%s' when %s are avaiable )" % (quantity, ownedBook.quantity, ))
        return redirect("/insertion")

    insState: Tuple[str, bool] = manageInsertion(usr, ownedBook, ownedBookOnSale, quantity, price, True)
    if not insState[1]:
        flash("An error occured during insertion's creation/update: " + insState[0])
        return redirect("/insertion")

    return redirect("/insertion")


@app.route("/insertion/unlist/", methods=['POST'])
def unlistbook() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/")

    (ownedBook, ownedBookOnSale, quantity, price) = retriveBooks(usr)
    if (quantity is None or price is None):
        flash("Missing parameters, be sure to compile them all")
        return redirect("/insertion")

    if ownedBookOnSale is None:
        flash("You aren't selling the selected book")
        return redirect("/insertion")

    if ownedBookOnSale.quantity < quantity or quantity <= 0:
        flash("You dont have enough books to unlist ('%s' when %s are avaiable )" % (quantity, ownedBookOnSale.quantity, ))
        return redirect("/insertion")

    insState: Tuple[str, bool] = manageInsertion(usr, ownedBook, ownedBookOnSale, quantity, price, False)
    if not insState[1]:
        flash("An error occured during insertion's deletion/update: " + insState[0])
        return redirect("/insertion")

    return redirect("/insertion")


def retriveBooks(usr:User) -> tuple[Own|None, Own|None, int|None, int|None]:
    """
    Returns the books owned by the user divided in not selling and slelling ones,
    the quantity requested by the user and the specified price
    """
    book: str|None = request.form.get("book") or None
    bookstate: str|None = request.form.get("bookstate") or None
    quantity: int|None = request.form.get("quantity", type=int) or None
    price: int|None = request.form.get("price", type=int) or None

    if book is None or bookstate is None or quantity is None or price is None:
        return None, None, None, None

    book = str(book)
    bookstate = str(bookstate)
    quantity = int(quantity)
    price = int(price)

    ownedBook: Own|None = db.session.scalar(sq.select(Own)
                                       .where(Own.fk_username == usr.username)
                                       .where(Own.fk_book == book)
                                       .where(Own.state == bookstate)
                                       .where(Own.price == None)
                                       )
    ownedBookOnSale: Own|None = db.session.scalar(sq.select(Own)
                                       .where(Own.fk_username == usr.username)
                                       .where(Own.fk_book == book)
                                       .where(Own.state == bookstate)
                                       .where(Own.price == price)
                                       )
    return ownedBook, ownedBookOnSale, quantity, price

def retriveExistingBooks(usr:User) -> tuple[Own|None, Own|None, int|None, int|None, int|None]:
    """
    Returns the books owned by the user divided in not selling and slelling ones,
    the quantity requested by the user and the specified old and new prices
    """
    book: str|None = request.form.get("book") or None
    bookstate: str|None = request.form.get("bookstate") or None
    quantity: int|None = request.form.get("quantity", type=int) or None
    oldprice: int|None = request.form.get("oldprice", type=int) or None
    newprice: int|None = request.form.get("newprice", type=int) or None

    if book is None or bookstate is None or quantity is None or oldprice is None:
        return None, None, None, None, None

    oldPriceBooks: Own|None = db.session.scalar(sq.select(Own)
                                       .where(Own.fk_username == usr.username)
                                       .where(Own.fk_book == book)
                                       .where(Own.state == bookstate)
                                       .where(Own.price == oldprice)
                                       )
    newPriceBooks: Own|None = db.session.scalar(sq.select(Own)
                                       .where(Own.fk_username == usr.username)
                                       .where(Own.fk_book == book)
                                       .where(Own.state == bookstate)
                                       .where(Own.price == newprice)
                                       )
    return oldPriceBooks, newPriceBooks, quantity, oldprice, newprice

def manageInsertion(usr: User, ownedBook: Own|None, ownedBookOnSale: Own|None, quantity:int, price:int|None, add:bool) -> Tuple[str, bool]:
    """
    This funtion manages the insertions.
    If add is positive, it will expext 'ownedBook' to be not None and it will
    create/update the insertions and/or delete the books that are not being sold as necessary.
    If add is negative, it will expect `ownedBookOnSale` to be not None and it will
    create/update the user's books that where being sold and/or delete the inserions.
    """
    if quantity <= 0:
        return "Requested quantity is less or eqaul to 0, doing nothing", False
    if price is None:
        return "A price was not guven to the function", False

    opreatinMsg: str
    try:
        if add and ownedBook is not None: # selling books
            if ownedBook.quantity == quantity:
                if ownedBookOnSale is not None:
                    ownedBookOnSale.quantity += quantity
                    opreatinMsg = f"Existing insertion has been updated with {{{quantity}}} more books, none remaining"
                else:
                    db.session.add(Own(
                        usr.username,
                        ownedBook.fk_book,
                        ownedBook.state,
                        price,
                        quantity
                    ))
                    opreatinMsg = f"New insertion has been created with {{{quantity}}} books, none remaining"
                db.session.delete(ownedBook)
            else:
                if ownedBookOnSale is not None:
                    ownedBookOnSale.quantity += quantity
                    opreatinMsg = f"Existing insertion has been updated with {{{quantity}}} more books, some remain to sell"
                else:
                    db.session.add(Own(
                        usr.username,
                        ownedBook.fk_book,
                        ownedBook.state,
                        price,
                        quantity
                    ))
                    opreatinMsg = f"New insertion has been created with {{{quantity}}} books, some remain to sell"
                ownedBook.quantity -= quantity
        elif not add and ownedBookOnSale is not None: # removing books from insertion
            if ownedBookOnSale.quantity == quantity:
                if ownedBook is not None:
                    ownedBook.quantity += quantity
                    opreatinMsg = f"Insertion has been deleted, {{{quantity}}} existing books added to library"
                else:
                    db.session.add(Own(
                        usr.username,
                        ownedBookOnSale.fk_book,
                        ownedBookOnSale.state,
                        None,
                        quantity
                    ))
                    opreatinMsg = f"Insertion has been deleted, {{{quantity}}} new books added to library"
                db.session.delete(ownedBookOnSale)

            else:
                if ownedBook is not None:
                    ownedBook.quantity += quantity
                    opreatinMsg = f"{{{quantity}}} existing books moved to the library, some remain listed"
                else:
                    db.session.add(Own(
                        usr.username,
                        ownedBookOnSale.fk_book,
                        ownedBookOnSale.state,
                        None,
                        quantity
                    ))
                    opreatinMsg = f"{{{quantity}}} new books moved to the library, some remain listed"
                ownedBookOnSale.quantity -= quantity
        else:
            db.session.rollback()
            return "Invalid state of owned/insertioned books passed to function", False
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return "An unexpected error occured while interacting with the database", False

    db.session.commit()
    return opreatinMsg, True
