from app.routes.auth import getLoggedInUser
from flask import current_app as app, render_template

@app.route("/")
def index() -> str:
    user = getLoggedInUser()
    return render_template("index.html", user=user)
