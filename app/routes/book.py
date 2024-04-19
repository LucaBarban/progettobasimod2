from flask import current_app as app, render_template, request
from app.models.book import Book
from app.database import db
import sqlalchemy as sq

@app.route("/book/")
def products() -> str:
    books = db.session.scalars(sq.select(Book))

    return render_template("books.html", books=books)

# /book/add?name=...&author=...
@app.route("/book/add")
def add() -> str:
    name = request.args.get("name")
    author = request.args.get("author")

    book = Book(name = name, author = author)

    db.session.add(book)
    db.session.commit()

    return f"<h1>Added {book.id}</h1>"

@app.route("/book/<int:id>")
def get(id: int) -> str:
    book = db.get_or_404(Book, id)
    print(book)

    return render_template("book.html", book=book)
