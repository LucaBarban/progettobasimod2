from typing import Optional

from sqlalchemy import ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.history import History
from app.models.user import User


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer, Sequence("notifications_id_seq"), primary_key=True
    )
    context: Mapped[str]
    fk_username: Mapped[str] = mapped_column(ForeignKey(User.username))
    message: Mapped[Optional[str]]
    archived: Mapped[bool]

    fk_history: Mapped[Optional[int]] = mapped_column(ForeignKey(History.id))
    order_status_old: Mapped[Optional[str]]
    order_status_new: Mapped[Optional[str]]
    order: Mapped[Optional[History]] = relationship()

    def __repr__(self) -> str:
        return f"Notification {{{self.id}, {self.fk_username}, {self.message}, archived: {self.archived} | [Order: {self.fk_history}, {self.order_status_old}, {self.order_status_new}]}}"


class NotificationCount(Base):
    __tablename__ = "notifications_count"

    username: Mapped[str] = mapped_column(String, primary_key=True)
    count: Mapped[int]

    def __repr__(self) -> str:
        return f"Notification Count: {{{self.username}, {self.count}}}"
