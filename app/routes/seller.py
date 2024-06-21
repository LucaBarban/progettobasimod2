import sqlalchemy as sq
from flask import current_app as app
from flask import render_template
from sqlalchemy import select

from app.database import db
from app.models.history import History
from app.models.own import Own
from app.models.user import User
from app.routes.auth import getLoggedInUser


@app.route("/seller/<string:username>")
def seller(username: str) -> str:
    """
    Display all the insertions on sale and the reviews for a specific seller
    404 if the searched user is not a seller
    """

    user = getLoggedInUser()

    seller = db.first_or_404(
        sq.select(User).filter(User.username == username, User.seller == True)
    )

    reviews = db.session.scalars(
        select(History).filter(History.fk_seller == username, History.review != None)
    ).all()

    insertions = db.session.scalars(
        select(Own)
        .distinct(Own.fk_book)
        .filter(Own.fk_username == username, Own.price != None)
    ).all()

    return render_template(
        "seller.html", user=user, seller=seller, reviews=reviews, insertions=insertions
    )
