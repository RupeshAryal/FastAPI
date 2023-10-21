"""create user tables

Revision ID: cf451349c94f
Revises: f09124df3e71
Create Date: 2023-10-21 13:47:34.687383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'cf451349c94f'
down_revision: Union[str, None] = 'f09124df3e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(2000), nullable=False),
        sa.Column("password", sa.String(300), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
