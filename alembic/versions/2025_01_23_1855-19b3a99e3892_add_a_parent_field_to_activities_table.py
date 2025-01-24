"""add a parent field to activities table

Revision ID: 19b3a99e3892
Revises: 3085753f356d
Create Date: 2025-01-23 18:55:25.578203

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19b3a99e3892"
down_revision: Union[str, None] = "3085753f356d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "activities", sa.Column("parent_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        op.f("fk_activities_parent_id_activities"),
        "activities",
        "activities",
        ["parent_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_activities_parent_id_activities"),
        "activities",
        type_="foreignkey",
    )
    op.drop_column("activities", "parent_id")
