from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "booksgenres"

    fk_idB: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True,)
    fk_genre: Mapped[str] = mapped_column(ForeignKey("genres.name"), primary_key=True)

    def __repr__(self) -> str:
        return f"Book-Genres {{{self.fk_idB}, {self.fk_genre}}}"
