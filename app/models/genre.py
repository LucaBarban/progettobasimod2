from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(primary_key=True)

    def __init__(self, name:str):
        self.name = name

    def __repr__(self) -> str:
        return f"Genre {{{self.name}}}"
