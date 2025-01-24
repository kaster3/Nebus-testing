"""create organizations table

Revision ID: b1e83d3da9b4
Revises: 62ef3b1bac39
Create Date: 2025-01-21 22:59:38.497031

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1e83d3da9b4"
down_revision: Union[str, None] = "62ef3b1bac39"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["buildings.id"],
            name=op.f("fk_organizations_building_id_buildings"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organizations")),
    )


def downgrade() -> None:
    op.drop_table("organizations")
