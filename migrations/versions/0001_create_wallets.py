"""create wallets table

Revision ID: 0001_create_wallets
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_create_wallets"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "wallets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "balance",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
            server_default="0",
        ),
    )
    op.create_index(
        op.f("ix_wallets_id"),
        "wallets",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_wallets_id"), table_name="wallets")
    op.drop_table("wallets")
