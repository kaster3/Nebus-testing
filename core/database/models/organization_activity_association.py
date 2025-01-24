from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin


class OrganizationActivityAssociation(Base, IntIdPkMixin):
    __tablename__ = "organization_activity_association"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "activity_id",
            name="index_unique_organization_activity",
        ),
    )

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
