from flask import current_app as app, render_template

@app.route("/")
def index() -> str:
    return render_template("index.html")
