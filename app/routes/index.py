from random import sample
from typing import List, Tuple

from flask import current_app as app
from flask import render_template

from sqlalchemy import select

from app.database import db
from app.models.book import Book
from app.models.genre import Genre
from app.routes.auth import getLoggedInUser


def generate_book_list(n_books: int = 5) -> List[Tuple[str, List[Book]]]:
    """
    Returns a list of random books by genre limited by ``n_books``
    """
    query = db.session.scalars(select(Genre)).all()
    books = [x for x in query if len(x.books) >= n_books]
    return [(genre.name, sample(genre.books, n_books)) for genre in books]


@app.route("/")
def index() -> str:
    user = getLoggedInUser()
    books = generate_book_list()
    return render_template("index.html", user=user, books=books)
