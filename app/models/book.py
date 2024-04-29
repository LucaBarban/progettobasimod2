from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    published: Mapped[date]
    pages: Mapped[int]
    isbn: Mapped[str]

    def __repr__(self) -> str:
        return f"Book {{ {self.id}, {self.title} }}"
