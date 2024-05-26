from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, db


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[date]
    last_logged_in_at: Mapped[datetime]
    balance: Mapped[int]
    seller: Mapped[bool]
    token: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User: {{{self.username}, {self.first_name}, {self.last_name}, {self.last_logged_in_at}, {self.seller}, {self.balance}, {self.password}, {self.token}}}"

    def unread_count(self) -> Optional[int]:
        from app.models.notification import NotificationCount

        nc = db.session.get(NotificationCount, self.username)

        if nc is None:
            return None

        return nc.count
