from flask import current_app as app
from flask import render_template

from app.book_list import BookListByGenre
from app.routes.auth import getLoggedInUser


@app.route("/")
def index() -> str:
    user = getLoggedInUser()
    books = BookListByGenre()
    books.prune(lambda x: len(x) < 5).normalize(
        lambda v: [x for i, x in enumerate(v) if i < 5]
    )
    return render_template("index.html", user=user, books=books.dump())
