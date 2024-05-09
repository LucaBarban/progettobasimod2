from sqlalchemy import ForeignKey, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.own import Own
from app.models.user import User


class Cart(Base):
    __tablename__ = "carts"

    fk_buyer: Mapped[str] = mapped_column(ForeignKey(User.username))
    fk_seller: Mapped[str] = mapped_column(
        ForeignKey(Own.fk_username), primary_key=True
    )
    fk_book: Mapped[int] = mapped_column(ForeignKey(Own.fk_book), primary_key=True)
    fk_state: Mapped[str] = mapped_column(ForeignKey(Own.state), primary_key=True)
    fk_price: Mapped[int] = mapped_column(ForeignKey(Own.price), primary_key=True)
    quantity: Mapped[int]

    own = relationship(
        Own,
        primaryjoin=and_(
            fk_seller == Own.fk_username,
            fk_book == Own.fk_book,
            fk_state == Own.state,
            fk_price == Own.price,
        ),
    )

    def __repr__(self) -> str:
        return f"Cart {{{self.fk_buyer}, {self.fk_seller}, {self.fk_book}, {self.fk_state}, {self.fk_price}, {self.quantity}}}"
