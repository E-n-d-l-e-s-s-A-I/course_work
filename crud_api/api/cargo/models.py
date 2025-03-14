import uuid as uuid_pkg

from database import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Cargo(Base):
    """Груз."""

    __tablename__ = "cargo"
    __table_args__ = {
        "comment": "Таблица с грузами",
        "info": {"readable_name": "Груз"},
    }

    id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid_pkg.uuid4,
        comment="Идентификатор груза",
    )
    name: Mapped[str] = mapped_column(
        comment="Название груза",
    )
    weight: Mapped[float] = mapped_column(
        comment="Вес груза",
    )
