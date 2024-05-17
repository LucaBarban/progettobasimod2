from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.author import Author
from app.models.genre import Genre
from app.models.publisher import Publisher


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    published: Mapped[date]
    pages: Mapped[int]
    isbn: Mapped[int]
    fk_author: Mapped[int] = mapped_column(ForeignKey(Author.id))
    fk_publisher: Mapped[str] = mapped_column(ForeignKey(Publisher.name))

    author: Mapped[Author] = relationship()
    publisher: Mapped[Publisher] = relationship()
    genres: Mapped[List[Genre]] = relationship(Genre, secondary="booksgenres")

    def __repr__(self) -> str:
        return f"Book {{{self.id}, {self.title}, {self.published}, {self.pages}, {self.isbn}, {self.fk_author}, {self.fk_publisher}}}"
