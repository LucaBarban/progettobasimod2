from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.author import Author
from app.models.publisher import Publisher


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    published: Mapped[date]
    pages: Mapped[int]
    isbn: Mapped[str]
    fk_author: Mapped[int] = mapped_column(ForeignKey(Author.id))
    fk_publisher: Mapped[str] = mapped_column(ForeignKey(Publisher.name))

    def __init__(self, title:str, published:date, pages:int, isbn:str, fk_author:int, fk_publisher:int):
        self.title = title
        self.published = published
        self.pages = pages
        self.isbn = isbn
        self.fk_author = fk_author
        self.fk_publisher = fk_publisher

    def __repr__(self) -> str:
        return f"Book {{{self.id},{self.title},{self.published},{self.pages},{self.isbn},{self.fk_author},{self.fk_publisher}}}"
