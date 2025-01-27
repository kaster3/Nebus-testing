from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models.base import Base
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from core.database.models import Organization


class PhoneNumber(IntIdPkMixin, Base):

    number: Mapped[str] = mapped_column(String(11))
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="phone_numbers",
    )

    def __repr__(self):
        return (
            f"<PhoneNumber(id={self.id}, number='{self.number}',"
            f" organization_id={self.organization_id})>"
        )
