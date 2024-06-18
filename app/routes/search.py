from dataclasses import dataclass
from typing import List, Optional

from flask import current_app as app
from flask import redirect, render_template, request
from sqlalchemy import or_
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from app.models.own import Own
from app.models.publisher import Publisher


@dataclass
class UserInput:
    search: str
    available: bool
    genres: List[str]
    publishers: List[str]
    min: Optional[float]
    max: Optional[float]


def generate_book_list(input: UserInput) -> List[Book]:
    query = db.session.query(Book).filter(
        or_(
            Book.title.icontains(input.search),
            Book.author.has(Author.first_name.icontains(input.search)),
            Book.author.has(Author.last_name.icontains(input.search)),
            Book.publisher.has(Publisher.name.icontains(input.search)),
        )
    )

    if len(input.genres):
        query = query.filter(Book.genres.any(Genre.name.in_(input.genres)))

    if len(input.publishers):
        query = query.filter(Book.publisher.has(Publisher.name.in_(input.publishers)))

    if input.available or input.min or input.max:
        query = query.join(Own)

        if input.available:
            query = query.filter(Own.price != None)
        if input.min:
            query = query.filter(Own.price >= input.min * 100.0)
        if input.max:
            query = query.filter(Own.price <= input.max * 100.0)

    return query.all()


@app.route("/search/", methods=["POST"])
def search() -> str | Response:
    user_input = request.form.get("user_input")

    if request.method != "POST" or user_input is None:
        return redirect("#")

    available = request.form.get("available") == "on"
    genres_input = request.form.getlist("genre")
    publishers_input = request.form.getlist("publisher")
    min = request.form.get("price_min")
    max = request.form.get("price_max")

    input = UserInput(
        search=user_input,
        available=available,
        genres=genres_input,
        publishers=publishers_input,
        min=None if min is None or min == "" else float(min),
        max=None if max is None or max == "" else float(max),
    )

    books = generate_book_list(input)

    genres = db.session.query(Genre).all()
    publishers = db.session.query(Publisher).all()

    return render_template(
        "search.html",
        user=None,
        books=books,
        input=input,
        genres=genres,
        publishers=publishers,
    )
