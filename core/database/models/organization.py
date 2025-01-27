from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Activity
from core.database.models.base import Base
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from core.database.models import Activity
    from core.database.models.buildings import Building
    from core.database.models.phone import PhoneNumber


class Organization(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(30))
    building_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("buildings.id", ondelete="CASCADE")
    )

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations",
        lazy="selectin",
    )

    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        "PhoneNumber",
        back_populates="organization",
    )

    activities: Mapped[list["Activity"]] = relationship(
        back_populates="organizations",
        secondary="organization_activity_association",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"
