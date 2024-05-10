from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book
from app.models.user import User


class Own(Base):
    __tablename__ = "owns"

    id: Mapped[int] = mapped_column(primary_key=True)
    fk_username: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_book: Mapped[str] = mapped_column(ForeignKey(Book.id))
    state: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int]

    user: Mapped[User] = relationship(User)
    book: Mapped[Book] = relationship(Book)

    __table_args__ = (UniqueConstraint(fk_username, fk_book, state, price),)

    def __repr__(self) -> str:
        return f"Own {{ {self.id}, {self.fk_username}, {self.fk_book}, {self.quantity}, {self.state}, {self.price} }}"
