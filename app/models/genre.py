from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Genre {{{self.name}}}"
