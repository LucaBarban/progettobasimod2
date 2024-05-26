from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book


class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(primary_key=True)
    books: Mapped[List[Book]] = relationship(
        Book, secondary="booksgenres", back_populates="genres"
    )

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Genre {{{self.name}, {self.books}}}"
