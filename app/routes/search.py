from typing import List

from flask import current_app as app
from flask import redirect, render_template, request
from sqlalchemy import or_
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from app.models.publisher import Publisher


def generate_book_list(
    input: str, genres: List[str], publishers: List[str]
) -> List[Book]:
    query = db.session.query(Book).filter(
        or_(
            Book.title.icontains(input),
            Book.author.has(Author.first_name.icontains(input)),
            Book.author.has(Author.last_name.icontains(input)),
            Book.publisher.has(Publisher.name.icontains(input)),
        )
    )

    if len(genres):
        query = query.filter(Book.genres.any(Genre.name.in_(genres)))
    if len(publishers):
        query = query.filter(Book.publisher.in_(publishers))

    return query.all()


@app.route("/search/", methods=["POST"])
def search() -> str | Response:
    user_input = request.form.get("user_input")

    if request.method != "POST" or user_input is None:
        return redirect("#")

    genres_input = request.form.getlist("genre")
    publishers_input = request.form.getlist("publisher")

    books = generate_book_list(user_input, genres_input, publishers_input)

    genres = db.session.query(Genre).all()

    publishers = db.session.query(Publisher).all()

    return render_template(
        "search.html",
        user=None,
        books=books,
        query=user_input,
        genres=genres,
        publishers=publishers,
    )
