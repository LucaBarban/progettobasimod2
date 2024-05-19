from flask import current_app as app
from flask import render_template

from app.database import db
from app.models.book import Book
from app.models.history import History
from app.models.own import Own
from app.routes.auth import getLoggedInUser


@app.route("/book/<int:id>")
def get(id: int) -> str:
    user = getLoggedInUser()

    if user is None:
        username = None
    else:
        username = user.username

    book = db.get_or_404(Book, id)

    insertions = db.session.query(Own).filter(
        Own.fk_book == id, Own.price != None, Own.fk_username != username
    )

    reviews = db.session.query(History).filter(
        History.fk_book == id, History.review != None
    )

    return render_template(
        "book.html", book=book, insertions=insertions, user=user, reviews=reviews
    )
