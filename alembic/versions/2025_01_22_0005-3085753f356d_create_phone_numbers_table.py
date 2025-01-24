"""create phone_numbers table

Revision ID: 3085753f356d
Revises: 7c3ed11e2b4e
Create Date: 2025-01-22 00:05:08.086268

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3085753f356d"
down_revision: Union[str, None] = "7c3ed11e2b4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "phone_numbers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(length=11), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f("fk_phone_numbers_organization_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_phone_numbers")),
    )


def downgrade() -> None:
    op.drop_table("phone_numbers")
