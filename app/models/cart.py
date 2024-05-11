from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.own import Own
from app.models.user import User


class Cart(Base):
    __tablename__ = "carts"

    fk_buyer: Mapped[str] = mapped_column(ForeignKey(User.username), primary_key=True)
    fk_own: Mapped[int] = mapped_column(ForeignKey(Own.id), primary_key=True)
    quantity: Mapped[int]

    own: Mapped[Own] = relationship(Own)

    def __repr__(self) -> str:
        return f"Cart {{{self.fk_buyer}, {self.own}, {self.quantity}}}"
