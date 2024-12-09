"""add change nullable of ticker

Revision ID: bfafb2265065
Revises: d2d9e2b4a7ef
Create Date: 2024-12-11 22:49:04.990245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfafb2265065'
down_revision: Union[str, None] = 'd2d9e2b4a7ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('naver_article_list', 'ticker',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('naver_article_list', 'ticker',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
