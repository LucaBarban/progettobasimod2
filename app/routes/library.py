from typing import List

import sqlalchemy as sq
from flask import current_app as app
from flask import redirect, render_template
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.own import Own
from app.routes.auth import getLoggedInUser


def page_list(current: int, last: int, offset: int = 2) -> List[int]:
    return list(range(max(1, current - offset), min(current + offset, last) + 1))


@app.route("/library/")
@app.route("/library/<int:page>")
def library(page: int = 1) -> str | Response:
    user = getLoggedInUser()
    if user is None:
        return redirect("/login")

    limit = 10

    count = db.session.query(Own).filter(Own.fk_username == user.username).count()

    last_page = count // limit + 1
    if (page - 1) * limit > count:
        page = last_page

    pages = page_list(page, last_page)

    owns = db.session.scalars(
        sq.select(Own)
        .filter(Own.fk_username == user.username)
        .limit(limit)
        .offset((page - 1) * limit)
    ).all()

    return render_template(
        "library.html",
        user=user,
        owns=owns,
        page=page,
        pages=pages,
        last_page=last_page,
    )
