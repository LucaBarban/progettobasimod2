from datetime import date as dt
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book
from app.models.user import User

Statuses = {"processing", "packing", "shipped", "on delivery", "delivered"}


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(
        Integer, Sequence("history_id_seq"), primary_key=True
    )
    date: Mapped[dt]
    quantity: Mapped[int]
    status: Mapped[str]
    price: Mapped[int]
    review: Mapped[Optional[str]]
    stars: Mapped[Optional[int]]
    fk_buyer: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_seller: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_book: Mapped[int] = mapped_column(ForeignKey(Book.id))
    state: Mapped[str]

    buyer: Mapped[User] = relationship(User, foreign_keys=[fk_buyer])
    seller: Mapped[User] = relationship(User, foreign_keys=[fk_seller])
    book: Mapped[Book] = relationship(Book)

    def __repr__(self) -> str:
        return f"History {{{self.id}, {self.date}, {self.quantity}, {self.status}, {self.review}, {self.fk_buyer}, {self.fk_seller}, {self.fk_book}, {self.state}}}"
