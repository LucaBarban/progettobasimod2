from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.book import Book
from app.models.user import User


class Own(Base):
    __tablename__ = "owns"

    fk_username: Mapped[str] = mapped_column(
        ForeignKey(User.username), primary_key=True
    )
    fk_book: Mapped[str] = mapped_column(ForeignKey(Book.id), primary_key=True)
    quantity: Mapped[int]
    state: Mapped[str] = mapped_column(primary_key=True)
    on_sale: Mapped[bool]

    user: Mapped[User] = relationship(User)
    book: Mapped[Book] = relationship(Book)

    def __repr__(self) -> str:
        return f"Own {{ {self.fk_username}, {self.fk_book}, {self.quantity}, {self.state}, {self.on_sale} }}"
