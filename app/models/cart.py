from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cart(Base):
    __tablename__ = "carts"

    fk_buyer: Mapped[str] = mapped_column(ForeignKey("users.username"), primary_key=True)
    fk_seller: Mapped[str] = mapped_column(ForeignKey("owns.fk_username"), primary_key=True)
    fk_book: Mapped[int] = mapped_column(ForeignKey("owns.fk_book"), primary_key=True)
    fk_state: Mapped[str] = mapped_column(ForeignKey("owns.state"))
    fk_sale: Mapped[bool] = mapped_column(ForeignKey("owns.on_sale"))
    quantity: Mapped[int]

    def __repr__(self) -> str:
        return f"Cart {{{self.fk_buyer}, {self.fk_seller}, {self.fk_book}, {self.fk_state}, {self.fk_sale}, {self.quantity}}}"
