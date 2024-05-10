from datetime import date as dt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

from app.models.user import User
from app.models.book import Book


class History(Base):
    __tablename__ = "history"

    idH: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[dt]
    quantity: Mapped[int]
    status: Mapped[str]
    recensione: Mapped[str]
    fk_buyer: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_seller: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_book: Mapped[int] = mapped_column(ForeignKey(Book.id))
    state: Mapped[str]

    def __repr__(self) -> str:
        return f"History {{{self.idH}, {self.date}, {self.quantity}, {self.status}, {self.recensione}, {self.fk_buyer}, {self.fk_seller}, {self.fk_book}, {self.state}}}"