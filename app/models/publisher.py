from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Publisher(Base):
    __tablename__ = "publishers"

    name: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Publisher {{ {self.name} }}"
