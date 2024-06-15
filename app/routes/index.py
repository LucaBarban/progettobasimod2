from random import sample
from typing import Generator, List, Tuple

from flask import current_app as app
from flask import render_template

from app.database import db
from app.models.book import Book
from app.models.genre import Genre
from app.routes.auth import getLoggedInUser


def generate_book_list(n_books: int = 5) -> List[Tuple[str, List[Book]]]:
    query = [x for x in db.session.query(Genre).all() if len(x.books) >= n_books]
    return [(genre.name, sample(genre.books, n_books)) for genre in query]


@app.route("/")
def index() -> str:
    user = getLoggedInUser()
    books = generate_book_list()
    return render_template("index.html", user=user, books=books)
