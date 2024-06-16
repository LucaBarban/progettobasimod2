from typing import Set

from flask import current_app as app
from flask import redirect, render_template, request
from sqlalchemy import or_
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.author import Author
from app.models.book import Book
from app.models.publisher import Publisher


def generate_book_list(query: str) -> Set[Book]:
    return set(
        db.session.query(Book)
        .filter(
            or_(
                Book.title.icontains(query),
                Book.author.has(Author.first_name.icontains(query)),
                Book.author.has(Author.last_name.icontains(query)),
                Book.publisher.has(Publisher.name.icontains(query)),
            )
        )
        .all()
    )


@app.route("/search/", methods=["POST"])
def search() -> str | Response:
    user_input = request.form.get("user_input")
    if request.method != "POST" or user_input is None:
        return redirect("#")

    books = generate_book_list(user_input)
    return render_template("search.html", user=None, books=books, query=user_input)
