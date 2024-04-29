from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[date]
    balance: Mapped[int]
    seller: Mapped[bool]

    def __repr__(self) -> str:
        return f"User {{ {self.username}, {self.balance}, {self.seller}"
