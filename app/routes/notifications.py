from flask import current_app as app
from flask import flash, redirect, render_template
from werkzeug.wrappers.response import Response

from app.database import db
from app.models.notification import Notification
from app.routes.auth import getLoggedInUser


@app.route("/notifications/read/", methods=["POST"])
def read_all_notifications() -> Response:
    """
    Set all the notifications for `user` as archived
    """

    user = getLoggedInUser()
    if user is None:
        return redirect("/login?link=/notifications")

    unreads = (
        db.session.query(Notification)
        .filter(
            Notification.fk_username == user.username, Notification.archived == False
        )
        .all()
    )

    for notif in unreads:
        notif.archived = True

    db.session.commit()

    return redirect("/notifications")


@app.route("/notifications/read/<int:id>", methods=["POST"])
def read_notification(id: int) -> Response:
    """
    Set a specific notification for `user` as archived
    """

    user = getLoggedInUser()

    notif = db.session.get(Notification, id)

    if user is None:
        return redirect("/login?link=/notifications")
    elif notif is None or notif.fk_username != user.username:
        # Trying to update the wrong notification
        flash("Notification not found", "error")
    else:
        notif.archived = True
        db.session.commit()

    return redirect("/notifications")


@app.route("/notifications/")
def notifications() -> str | Response:
    """
    Display all the notifications for a user, grouped by new and archived
    """

    user = getLoggedInUser()
    if user is None:
        return redirect("/login?link=/notifications")

    unreads = (
        db.session.query(Notification)
        .filter(
            Notification.fk_username == user.username, Notification.archived == False
        )
        .all()
    )

    archived = (
        db.session.query(Notification)
        .filter(
            Notification.fk_username == user.username, Notification.archived == True
        )
        .all()
    )

    return render_template(
        "notifications.html", user=user, unreads=unreads, archived=archived
    )
