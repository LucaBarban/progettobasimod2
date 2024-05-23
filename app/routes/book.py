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
from sqlalchemy import exc

@app.route("/book/")
def products() -> str:
    books = db.session.scalars(sq.select(Book))

    return render_template("books.html", books=books)

@app.route("/book/add", methods=['GET', 'POST'])
def add() -> str|Response:
    usr: User|None = getLoggedInUser()
    if usr is None:
        return redirect("/login/?link=/book/add")

    genres = db.session.scalars(sq.select(Genre)).fetchall()
    authors = db.session.scalars(sq.select(Author)).fetchall()
    publishers = db.session.scalars(sq.select(Publisher)).fetchall()

    if request.method != 'POST':
        return render_template("bookadd.html", user=usr, genres=genres, authors=authors, publishers=publishers)

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
        return render_template("bookadd.html", user=usr, genres=genres, authors=authors, publishers=publishers)

    book: Book
    author: Author|None = next((a for a in authors if a.id == authorid), None) # next iterates untill the iterator provided by the foor loop iterates afer the whole list
    publisher: Publisher|None = next((p for p in publishers if p.name == publishername), None)
    if author is None or publisher is None:
        flash("An unforeseen error occurred")
        return render_template("bookadd.html", user=usr, genres=genres, authors=authors, publishers=publishers)

    try:
        book = Book(title, published, pages, isbn, author, publisher)
        db.session.add(book)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        flash("An error occured while adding the new book")

    return render_template("bookadd.html", user=usr, genres=genres, authors=authors, publishers=publishers)

@app.route("/book/<int:id>")
def get(id: int) -> str:
    book = db.get_or_404(Book, id)
    print(book)

    return render_template("book.html", book=book)

def checkIsbn(isbn:str) -> bool:
    """
    Function used to check if a given ISBN code is correct. This
    has been borrowed from https://stackoverflow.com/a/4047709
    """
    isbn = isbn.replace("-", "").replace(" ", "").upper()
    match = re.search(r'^(\d{9})(\d|X)$', isbn)
    if not match:
        return False

    digits = match.group(1)
    check_digit = 10 if match.group(2) == 'X' else int(match.group(2))

    result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
    return (result % 11) == check_digit
