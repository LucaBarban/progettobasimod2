from random import randint
from typing import List

from flask import current_app as app
from flask import render_template

from app.database import db
from app.models.genre import Genre
from app.routes.auth import getLoggedInUser


def generate_book_list(n_books: int = 5) -> List[Genre]:
    query = [x for x in db.session.query(Genre).all() if len(x.books) >= n_books]
    for x in query:
        if len(x.books) >= n_books:
            books = []
            for _ in range(n_books):
                while True:
                    index = randint(0, len(x.books) - 1)
                    book = x.books[index]
                    if book not in books:
                        break
                books.append(book)
            x.books = books
    return query


@app.route("/")
def index() -> str:
    user = getLoggedInUser()
    books = generate_book_list()
    return render_template("index.html", user=user, books=books)
