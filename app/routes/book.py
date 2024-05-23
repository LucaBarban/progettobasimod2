from datetime import date, datetime
import re
from flask import current_app as app, flash, render_template, request, redirect
from app.routes.auth import getLoggedInUser #type: ignore
from werkzeug.wrappers.response import Response
from app.models.book import Book
from app.models.user import User
from app.models.genre import Genre
from app.models.publisher import Publisher
from app.models.author import Author
from app.database import db
import sqlalchemy as sq
from sqlalchemy import and_, exc

@app.route("/book/")
def products() -> Response:

    return redirect("/library/")

@app.route("/book/add/", methods=['GET', 'POST'])
def add() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add")

    genres = db.session.scalars(sq.select(Genre)).fetchall()
    authors = db.session.scalars(sq.select(Author)).fetchall()
    publishers = db.session.scalars(sq.select(Publisher)).fetchall()

    if request.method != 'POST':
        return render_template("addbook.html", user=usr, genres=genres, authors=authors, publishers=publishers)

    title: str|None = request.form.get("title") or None
    published: date|None
    try:
        published = datetime.strptime(request.form.get("published") or "", '%Y-%m-%d')
    except ValueError:
        published = None
    pages: int = int(request.form.get("pages") or -1)
    isbn: str|None = request.form.get("isbn") or None
    authorid: int|None = int(request.form.get("author") or -1)
    publishername: str|None =  request.form.get("publisher") or None
    selectedGenres: list[str] = request.form.getlist("genres")

    if title is None :
        flash("The title has been found to be empty")
    if published is None :
        flash("The date of pubblication is invalid")
    if pages <= 0:
        flash("The number of pages is invalid")
    if isbn is None or not checkIsbn(isbn):
        isbn = None
        flash("Provide a valid ISBN code")
    if authorid is None:
        flash("An author has to be set")
    if publishername is None:
        flash("A publisher has to be set")
    if len(selectedGenres) == 0:
        flash("Select at least one genre")
    if title is None or published is None or pages <= 0 or isbn is None or authorid is None or publishername is None or len(selectedGenres) == 0:
        return render_template("addbook.html", user=usr, genres=genres, authors=authors, publishers=publishers)

    book: Book
    author: Author|None = next((a for a in authors if a.id == authorid), None) # next iterates untill the iterator provided by the foor loop iterates afer the whole list
    publisher: Publisher|None = next((p for p in publishers if p.name == publishername), None)
    if author is None or publisher is None:
        flash("An unforeseen error occurred")
        return render_template("addbook.html", user=usr, genres=genres, authors=authors, publishers=publishers)

    try:
        book = Book(title, published, pages, isbn, author, publisher)
        db.session.add(book)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        flash("An error occured while adding the new book")

    return render_template("addbook.html", user=usr, genres=genres, authors=authors, publishers=publishers)

@app.route("/book/<int:id>")
def get(id: int) -> str:
    book = db.get_or_404(Book, id)
    print(book)

    return render_template("book.html", book=book)

@app.route("/book/add/genre/", methods=['GET', 'POST'])
def addgenre() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/genre")

    if request.method == 'POST':
        genrename: str|None = request.form.get("name") or None
        if genrename is None:
            flash("You must compile the genre field")
        else:
            try:
                genre = Genre(genrename)
                db.session.add(genre)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new genre")

            flash("Genre added correctly")
            return redirect("/book/add/")

    return render_template("addgenre.html", user=usr)

@app.route("/book/add/publisher/", methods=['GET', 'POST'])
def addpublisher() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/publisher")

    if request.method == 'POST':
        publishername: str|None = request.form.get("name") or None
        if publishername is None:
            flash("You must compile the publisher field")
        else:
            try:
                publisher = Publisher(publishername)
                db.session.add(publisher)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new publisher")

            flash("Publisher added correctly")
            return redirect("/book/add/")

    return render_template("addpublisher.html", user=usr)

@app.route("/book/add/author/", methods=['GET', 'POST'])
def addauthor() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add/author")

    if request.method == 'POST':
        first_name: str|None = request.form.get("first_name") or None
        last_name: str|None = request.form.get("last_name") or None

        if first_name is None or last_name is None:
            flash("You must compile all the fields")
        else:
            try:
                if len(db.session.scalars(sq.select(Author)
                                          .filter(and_
                                              (Author.first_name == first_name,
                                               Author.last_name == last_name)
                                          )).fetchall()) != 0:
                    flash("Author already exists")
                    return redirect("/book/add/author/")

                author = Author(first_name, last_name)
                db.session.add(author)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occured while adding the new author")

            flash("Author added correctly")
            return redirect("/book/add/")

    return render_template("addauthor.html", user=usr)

def checkIsbn(isbn:str) -> bool:
    """
    Function used to check if a given ISBN code is correct. This
    has been borrowed from https://stackoverflow.com/a/4047709
    """
    isbn = isbn.replace("-", "").replace(" ", "").upper()
    match = re.search(r'^(\d{9})(\d|X)$', isbn) # treating the string as raw (things like \ are treated as literal characters)
                                                # from the start of the string (^) take 9 characters (\d{9}) and a tenth that
                                                # can also be an X

    if not match:
        return False

    digits = match.group(1)
    check_digit = 10 if match.group(2) == 'X' else int(match.group(2))

    result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
    return (result % 11) == check_digit
