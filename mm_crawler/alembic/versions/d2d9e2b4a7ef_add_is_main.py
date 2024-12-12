"""add is main

Revision ID: d2d9e2b4a7ef
Revises: 124d717f8267
Create Date: 2024-12-11 22:43:45.533828

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd2d9e2b4a7ef'
down_revision: Union[str, None] = '124d717f8267'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('naver_main_article_list')
    op.drop_index('ix_cmetadata_gin', table_name='langchain_pg_embedding', postgresql_using='gin')
    op.drop_index('ix_langchain_pg_embedding_id', table_name='langchain_pg_embedding')
    op.drop_table('langchain_pg_embedding')
    op.drop_table('langchain_pg_collection')
    op.add_column('naver_article_list', sa.Column('is_main', sa.Boolean(), nullable=True))
    op.alter_column('naver_article_list', 'is_origin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('naver_article_list', 'is_origin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('naver_article_list', 'is_main')
    op.create_table('langchain_pg_collection',
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('cmetadata', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='langchain_pg_collection_pkey'),
    sa.UniqueConstraint('name', name='langchain_pg_collection_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('langchain_pg_embedding',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('collection_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(), autoincrement=False, nullable=True),
    sa.Column('document', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cmetadata', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['langchain_pg_collection.uuid'], name='langchain_pg_embedding_collection_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='langchain_pg_embedding_pkey')
    )
    op.create_index('ix_langchain_pg_embedding_id', 'langchain_pg_embedding', ['id'], unique=True)
    op.create_index('ix_cmetadata_gin', 'langchain_pg_embedding', ['cmetadata'], unique=False, postgresql_using='gin')
    op.create_table('naver_main_article_list',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('article_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('media_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('media_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('link', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('article_published_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('latest_scraped_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='naver_main_article_list_pkey')
    )
    # ### end Alembic commands ###
