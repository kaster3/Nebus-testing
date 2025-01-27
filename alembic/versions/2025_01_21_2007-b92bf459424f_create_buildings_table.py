"""create buildings table

Revision ID: b92bf459424f
Revises:
Create Date: 2025-01-21 20:07:00.808853

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "b92bf459424f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=20), nullable=False),
        sa.Column("street", sa.String(length=40), nullable=False),
        sa.Column("house_number", sa.String(length=5), nullable=False),
        sa.Column("apartment_number", sa.Integer(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_buildings")),
    )


def downgrade() -> None:
    op.drop_table("buildings")
