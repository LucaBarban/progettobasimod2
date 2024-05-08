from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    def __repr__(self) -> str:
        return f"Author {{{self.id}, {self.first_name}, {self.last_name}}}"
