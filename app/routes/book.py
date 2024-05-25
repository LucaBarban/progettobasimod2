from datetime import date, datetime
import os
import re
from typing import List
from flask import current_app as app, flash, render_template, request, redirect
from app.book_list import AllowedExtensions
from app.routes.auth import getLoggedInUser  # type: ignore
from werkzeug.wrappers.response import Response
from app.models.book import Book
from app.models.user import User
from app.models.genre import Genre
from app.models.publisher import Publisher
from app.models.author import Author
from app.models.own import Own
from app.models.history import History
from app.database import db
import sqlalchemy as sq
from sqlalchemy import and_, exc
from stdnum import isbn as isbnval  # type: ignore


@app.route("/book/")
def products() -> Response:
    return redirect("/library/")


@app.route("/book/<int:id>/")
def get(id: int) -> str:
    user = getLoggedInUser()

    if user is None:
        username = None
    else:
        username = user.username

    book = db.get_or_404(Book, id)

    insertions = db.session.query(Own).filter(
        Own.fk_book == id, Own.price != None, Own.fk_username != username
    )

    reviews = db.session.query(History).filter(History.fk_book == id)

    return render_template(
        "book.html", book=book, insertions=insertions, user=user, reviews=reviews
    )


@app.route("/book/add/", methods=["GET", "POST"])
def add() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add")

    genres = db.session.scalars(sq.select(Genre)).fetchall()
    authors = db.session.scalars(sq.select(Author)).fetchall()
    publishers = db.session.scalars(sq.select(Publisher)).fetchall()

    if request.method != "POST":
        return render_template(
            "addbook.html",
            user=usr,
            genres=genres,
            authors=authors,
            publishers=publishers,
        )

    title: str | None = request.form.get("title") or None
    published: date | None
    try:
        published = datetime.strptime(request.form.get("published") or "", "%Y-%m-%d")
    except ValueError:
        published = None
    pages: int = int(request.form.get("pages") or -1)
    isbn: str | None = request.form.get("isbn") or None
    authorid: int | None = int(request.form.get("author") or -1)
    publishername: str | None = request.form.get("publisher") or None
    selectedGenres: list[str] = request.form.getlist("genres")

    if title is None:
        flash("The title has been found to be empty")
    if published is None:
        flash("The date of pubblication is invalid")
    if pages <= 0:
        flash("The number of pages is invalid")
    isbres: bool = False
    if isbn is not None:
        try:
            isbres = isbnval.is_valid(isbn)
        except:
            pass
    if not isbres:
        flash("Provide a valid ISBN code (" + str(isbn) + ")")
    if authorid is None:
        flash("An author has to be set")
    if publishername is None:
        flash("A publisher has to be set")
    if len(selectedGenres) == 0:
        flash("Select at least one genre")
    tmpfilename: str = ""
    tmpfileextension: str = ""
    if "file" not in request.files:
        flash("Book's cover is missing")
    elif request.files["file"].filename == "":
        flash("Select a file to upload as the book's cover")
    else:
        tmpfilename = str(request.files["file"].filename)
        tmpfileextension = tmpfilename.rsplit(".", 1)[-1].lower()
        if "." in tmpfilename and tmpfileextension not in AllowedExtensions:
            flash("Invalid file extension")
            tmpfilename = ""
    if (
        title is None
        or published is None
        or pages <= 0
        or not isbres
        or authorid is None
        or publishername is None
        or len(selectedGenres) == 0
        or tmpfilename == ""
    ):
        return render_template(
            "addbook.html",
            user=usr,
            genres=genres,
            authors=authors,
            publishers=publishers,
        )

    isbn = str(isbnval.validate(isbn))
    book: Book
    author: Author | None = next(
        (a for a in authors if a.id == authorid), None
    )  # next iterates untill the iterator provided by the foor loop iterates afer the whole list
    publisher: Publisher | None = next(
        (p for p in publishers if p.name == publishername), None
    )
    bookgenres: List[Genre] = []
    for sgen in selectedGenres:
        for g in genres:
            if sgen == g.name:
                bookgenres.append(g)
    bookcover = request.files["file"]

    if author is None or publisher is None:
        flash("An unforeseen error occurred")
        return render_template(
            "addbook.html",
            user=usr,
            genres=genres,
            authors=authors,
            publishers=publishers,
        )

    try:
        book = Book(title, published, pages, isbn, author, publisher, bookgenres)
        db.session.add(book)
        db.session.flush()
        bookcover.save(
            os.path.join(app.config["UPLOAD_FOLDER"], f"{book.id}.{tmpfileextension}")
        )
        db.session.commit()
        flash("Book added correctly")
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        flash("An error occured while adding the new book")
    except:
        db.session.rollback()
        flash("An unhandled error occured while adding the new book")

    return render_template(
        "addbook.html", user=usr, genres=genres, authors=authors, publishers=publishers
    )


@app.route("/book/add/genre/", methods=["GET", "POST"])
def addgenre() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/genre")

    if request.method == "POST":
        genrename: str | None = request.form.get("name") or None
        if genrename is None:
            flash("You must compile the genre field")
        else:
            try:
                genre = Genre(genrename)
                db.session.add(genre)
                db.session.commit()
                flash("Genre added correctly")
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new genre")

            return redirect("/book/add/")

    return render_template("addgenre.html", user=usr)


@app.route("/book/add/publisher/", methods=["GET", "POST"])
def addpublisher() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/publisher")

    if request.method == "POST":
        publishername: str | None = request.form.get("name") or None
        if publishername is None:
            flash("You must compile the publisher field")
        else:
            try:
                publisher = Publisher(publishername)
                db.session.add(publisher)
                db.session.commit()
                flash("Publisher added correctly")
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new publisher")

            return redirect("/book/add/")

    return render_template("addpublisher.html", user=usr)


@app.route("/book/add/author/", methods=["GET", "POST"])
def addauthor() -> str | Response:
    usr: User | None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/author")

    if request.method == "POST":
        first_name: str | None = request.form.get("first_name") or None
        last_name: str | None = request.form.get("last_name") or None

        if first_name is None or last_name is None:
            flash("You must compile all the fields")
        else:
            try:
                if (
                    db.session.scalars(
                        sq.select(Author).filter(
                            and_(
                                Author.first_name == first_name,
                                Author.last_name == last_name,
                            )
                        )
                    ).one_or_none()
                    is not None
                ):
                    flash("Author already exists")
                    return redirect("/book/add/author/")

                author = Author(first_name, last_name)
                db.session.add(author)
                db.session.commit()
                flash("Author added correctly")
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new author")

            return redirect("/book/add/")

    return render_template("addauthor.html", user=usr)
