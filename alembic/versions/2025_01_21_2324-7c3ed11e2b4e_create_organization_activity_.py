"""create organization_activity_association table

Revision ID: 7c3ed11e2b4e
Revises: b1e83d3da9b4
Create Date: 2025-01-21 23:24:01.199384

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c3ed11e2b4e"
down_revision: Union[str, None] = "b1e83d3da9b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organization_activity_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activities.id"],
            name=op.f(
                "fk_organization_activity_association_activity_id_activities"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f(
                "fk_organization_activity_association_organization_id_organizations"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_organization_activity_association")
        ),
        sa.UniqueConstraint(
            "organization_id",
            "activity_id",
            name="index_unique_organization_activity",
        ),
    )


def downgrade() -> None:
    op.drop_table("organization_activity_association")
