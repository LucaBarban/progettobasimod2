from sqlalchemy import ForeignKey, Integer, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.history import History


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer, Sequence("notifications_id_seq"), primary_key=True
    )
    fk_order: Mapped[int] = mapped_column(ForeignKey(History.id))
    message: Mapped[str]
    archived: Mapped[bool]

    order: Mapped[History] = relationship()

    def __repr__(self) -> str:
        return f"Notification {{{self.id}, {self.fk_order}, {self.message}, archived: {self.archived} -> {self.order}}}"
