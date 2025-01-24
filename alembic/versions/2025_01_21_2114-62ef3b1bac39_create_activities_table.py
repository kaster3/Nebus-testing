"""create activities table

Revision ID: 62ef3b1bac39
Revises: b92bf459424f
Create Date: 2025-01-21 21:14:49.089028

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62ef3b1bac39"
down_revision: Union[str, None] = "b92bf459424f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_activities")),
    )


def downgrade() -> None:
    op.drop_table("activities")
