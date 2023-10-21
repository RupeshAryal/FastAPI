"""add foreign key in votes table

Revision ID: d656ed5ada4a
Revises: 64c3b6b4d5bb
Create Date: 2023-10-21 14:26:11.156623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd656ed5ada4a'
down_revision: Union[str, None] = '64c3b6b4d5bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key("vote_post_fk", "votes", referent_table="posts", local_cols=['post_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key("vote_user_fk", "votes", referent_table="users", local_cols=['user_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
   op.drop_constraint("vote_user_fk", table_name="votes")
   op.drop_constraint("vote_post_fk", table_name="votes")

   pass
