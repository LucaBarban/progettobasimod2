from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.book import Book
from app.models.genre import Genre

class Booksgenre(Base):
    __tablename__ = "booksgenres"

    fk_idb: Mapped[int] = mapped_column(
        ForeignKey(Book.id),
        primary_key=True,
    )
    fk_genre: Mapped[str] = mapped_column(
        ForeignKey(Genre.name),
        primary_key=True)

    def __repr__(self) -> str:
        return f"Book-Genres {{{self.fk_idb}, {self.fk_genre}}}"

