"""update relationships

Revision ID: 52662ec8a6e5
Revises: a941d05aec0f
Create Date: 2024-12-09 23:01:55.006693

"""
from typing import Sequence, Union

import pgvector.sqlalchemy
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '52662ec8a6e5'
down_revision: Union[str, None] = 'a941d05aec0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('naver_article_contents', sa.Column('embedded_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('naver_research_report_files', 'embedded_at')
    op.add_column('naver_research_reports', sa.Column('embedded_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('naver_research_reports', 'embedded_at')
    op.add_column('naver_research_report_files', sa.Column('embedded_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('naver_article_contents', 'embedded_at')
    # ### end Alembic commands ###
