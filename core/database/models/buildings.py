from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models.base import Base
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from core.database.models import Organization


class Building(IntIdPkMixin, Base):
    city: Mapped[str] = mapped_column(String(20))
    street: Mapped[str] = mapped_column(String(40))
    house_number: Mapped[str] = mapped_column(String(5))
    apartment_number: Mapped[int | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="building"
    )

    def __repr__(self):
        return (
            f"<Building({self.id=}, {self.city=}, {self.street=}, "
            f"{self.house_number=}, {self.apartment_number=} "
            f"{self.latitude=}, {self.longitude=})>"
        )
