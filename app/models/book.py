from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.author import Author
from app.models.publisher import Publisher

if TYPE_CHECKING:
    from app.models.genre import Genre
else:
    Genre = "Genre"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    published: Mapped[date]
    pages: Mapped[int]
    isbn: Mapped[Optional[str]]
    fk_author: Mapped[int] = mapped_column(ForeignKey(Author.id))
    fk_publisher: Mapped[str] = mapped_column(ForeignKey(Publisher.name))

    author: Mapped[Author] = relationship()
    publisher: Mapped[Publisher] = relationship()
    genres: Mapped[List[Genre]] = relationship(
        Genre, secondary="booksgenres", back_populates="books"
    )

    def __init__(
        self,
        title: str,
        published: date,
        pages: int,
        isbn: str | None,
        author: Author,
        publisher: Publisher,
        genres: List[Genre],
    ):
        self.title = title
        self.published = published
        self.pages = pages
        self.isbn = isbn
        self.author = author
        self.publisher = publisher
        self.genres = genres

    def display_generes(self) -> str:
        return ", ".join(tuple(x.name for x in self.genres))

    def __repr__(self) -> str:
        return f"Book {{{self.id}, {self.title}, {self.published}, {self.pages}, {self.isbn}, {self.fk_author}, {self.fk_publisher}}}"
