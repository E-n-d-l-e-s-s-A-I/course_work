import uuid as uuid_pkg

from database import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class City(Base):
    """Город."""

    __tablename__ = "city"
    __table_args__ = {
        "comment": "Таблица с городами",
        "info": {"readable_name": "Город"},
    }

    id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid_pkg.uuid4,
        comment="Идентификатор города",
    )
    name: Mapped[str] = mapped_column(
        comment="Название города",
        unique=True,
    )
