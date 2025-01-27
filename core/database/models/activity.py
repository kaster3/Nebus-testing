from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models.base import Base
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from core.database.models import Organization


class Activity(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("activities.id"))

    parent = relationship("Activity", remote_side="Activity.id", backref="children")

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="activities",
        secondary="organization_activity_association",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"
