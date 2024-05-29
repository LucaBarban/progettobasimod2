from typing import Optional

from sqlalchemy import ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.history import History
from app.models.user import User


class Star(Base):
    __tablename__ = "star_count"

    fk_seller: Mapped[str] = mapped_column(ForeignKey(User.username), primary_key=True)
    vote: Mapped[float]

    seller: Mapped[User] = relationship(User, foreign_keys=[fk_seller])

    def __repr__(self) -> str:
        return f"Star {{{self.fk_seller}, {self.vote}}}"
