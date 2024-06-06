import sqlalchemy as sq
from flask import current_app as app
from flask import render_template

from app.database import db
from app.models.history import History
from app.models.user import User
from app.routes.auth import getLoggedInUser


@app.route("/seller/<string:username>")
def seller(username: str) -> str:
    user = getLoggedInUser()

    seller = db.first_or_404(
        sq.select(User).filter(User.username == username, User.seller == True)
    )

    reviews = db.session.query(History).filter(
        History.fk_seller == username, History.review != None
    )

    return render_template("seller.html", user=user, seller=seller, reviews=reviews)
