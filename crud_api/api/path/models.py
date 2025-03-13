import uuid as uuid_pkg
from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


from api.city.models import City


class Path(Base):
    """Путь."""

    __tablename__ = "path"
    __table_args__ = {
        "comment": "Таблица с путями",
    }

    id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid_pkg.uuid4,
        comment="Идентификатор пути",
    )
    city_from_id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        ForeignKey("city.id"),
        default=None,
        index=True,
        nullable=False,
        comment="Идентификатор города отправления",
    )
    city_to_id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        ForeignKey("city.id"),
        default=None,
        index=True,
        nullable=False,
        comment="Идентификатор города прибытия",
    )
    distance: Mapped[float] = mapped_column(
        comment="Протяженность пути",
    )
    max_weight: Mapped[float] = mapped_column(
        comment="Максимально допустимый вес на пути",
    )
    max_height: Mapped[float] = mapped_column(
        comment="Максимально допустимая высота на пути",
    )

    city_from: Mapped[City] = relationship(lazy="joined", foreign_keys=[city_from_id])
    city_to: Mapped[City] = relationship(lazy="joined", foreign_keys=[city_to_id])
