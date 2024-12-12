"""change nullability

Revision ID: 126a6544371c
Revises: bfafb2265065
Create Date: 2024-12-11 23:01:46.261199

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '126a6544371c'
down_revision: Union[str, None] = 'bfafb2265065'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('naver_article_contents', 'article_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('naver_article_list', 'is_origin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('naver_article_list', 'is_origin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('naver_article_contents', 'article_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
