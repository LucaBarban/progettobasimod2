from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    published: Mapped[date]
    pages: Mapped[int]
    isbn: Mapped[int]
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    publisher: Mapped[str] = mapped_column(ForeignKey("publishers.name"))

    def __repr__(self) -> str:
        return f"Book {{{self.id},{self.title},{self.published},{self.pages},{self.isbn},{self.author},{self.publisher}}}"
