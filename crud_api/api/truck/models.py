import uuid as uuid_pkg

from database import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Truck(Base):
    """Грузовик."""

    __tablename__ = "truck"
    __table_args__ = {
        "comment": "Таблица с грузовиками",
        "info": {"readable_name": "Грузовик"},
    }

    id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid_pkg.uuid4,
        comment="Идентификатор грузовика",
    )
    name: Mapped[str] = mapped_column(
        comment="Название грузовика",
        unique=True,
    )
    weight: Mapped[float] = mapped_column(
        comment="Вес грузовика",
    )
    speed: Mapped[float] = mapped_column(
        comment="Скорость грузовика",
    )
    height: Mapped[float] = mapped_column(
        comment="Высота грузовика",
    )
    max_cargo_weight: Mapped[float] = mapped_column(
        comment="Максимальный вес груза",
    )
