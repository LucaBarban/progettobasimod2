from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user import User


class Star(Base):
    __tablename__ = "star_count"

    fk_seller: Mapped[str] = mapped_column(ForeignKey(User.username), primary_key=True)
    vote: Mapped[float]
    total: Mapped[int]

    seller: Mapped[User] = relationship(User, foreign_keys=[fk_seller])

    def __repr__(self) -> str:
        return f"Star {{{self.fk_seller}, {self.vote}}}"
