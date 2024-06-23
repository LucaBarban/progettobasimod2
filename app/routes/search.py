from dataclasses import dataclass
from typing import List, Optional

from flask import current_app as app
from flask import render_template, request
from sqlalchemy import or_, select
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from app.models.own import Own
from app.models.publisher import Publisher
from app.routes.auth import getLoggedInUser


@dataclass
class UserInput:
    search: str
    available: bool
    genres: List[str]
    publishers: List[str]
    min: Optional[float]
    max: Optional[float]


def generate_book_list(input: UserInput) -> List[Book]:
    """
    Returns a list of all the books that matched the `UserInput` filters
    """

    # Filter for searchbar, match in title, author first and last name and publisher
    query = select(Book).filter(
        or_(
            Book.title.icontains(input.search),
            Book.author.has(Author.first_name.icontains(input.search)),
            Book.author.has(Author.last_name.icontains(input.search)),
            Book.publisher.has(Publisher.name.icontains(input.search)),
        )
    )

    # If filter by genres, keep any books that contains these genres
    if len(input.genres):
        query = query.filter(Book.genres.any(Genre.name.in_(input.genres)))

    # If filter by publishers, keep any books that contains these publishers
    if len(input.publishers):
        query = query.filter(Book.publisher.has(Publisher.name.in_(input.publishers)))

    # If filters by insertions
    if input.available or input.min or input.max:
        query = query.join(Own)

        if input.available:
            query = query.filter(Own.price != None)  # Keep only the books on sale
        if input.min:
            # Keep only the books with price >= min price
            query = query.filter(Own.price >= input.min * 100.0)
        if input.max:
            # Keep only the books with price <= max price
            query = query.filter(Own.price <= input.max * 100.0)

    # to prevent mypy to complain
    return list(db.session.scalars(query).all())


@app.route("/search/", methods=["POST"])
def search() -> str | Response:
    """
    Parse search form and returns all the matching books
    """

    user = getLoggedInUser()

    user_input = request.form.get("user_input") or ""
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
    )  # Convert prices to float or keep them as None

    # Filtered books list
    books = generate_book_list(input)

    # Needed to fill the checkboxes automatically
    genres = db.session.scalars(select(Genre)).all()
    publishers = db.session.scalars(select(Publisher)).all()

    return render_template(
        "search.html",
        user=user,
        books=books,
        input=input,
        genres=genres,
        publishers=publishers,
    )
