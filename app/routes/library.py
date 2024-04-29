from typing import List

import sqlalchemy as sq
from flask import current_app as app
from flask import render_template

from app.database import db
from app.models.own import Own


def page_list(current: int, last: int, offset: int = 2) -> List[int]:
    return list(range(max(1, current - offset), min(current + offset, last) + 1))


@app.route("/library/")
@app.route("/library/<int:page>")
def library(page: int = 1) -> str:
    username = "user_B"

    limit = 2

    count = db.session.query(Own).filter(Own.fk_username == username).count()

    last_page = count // limit + 1
    if (page - 1) * limit > count:
        page = last_page

    pages = page_list(page, last_page)

    owns = db.session.scalars(
        sq.select(Own)
        .filter(Own.fk_username == username)
        .limit(limit)
        .offset((page - 1) * limit)
    ).all()

    return render_template(
        "library.html", username=username, owns=owns, pages=pages, last_page=last_page
    )
