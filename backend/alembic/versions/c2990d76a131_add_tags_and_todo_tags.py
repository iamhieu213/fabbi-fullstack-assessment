"""add_tags_and_todo_tags

Revision ID: c2990d76a131
Revises: b1880c76a130
Create Date: 2026-09-16 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c2990d76a131'
down_revision: Union[str, None] = 'b1880c76a130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'tags',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_tags_user_id', 'tags', ['user_id'])
    # Case-insensitive unique constraint for PostgreSQL
    op.execute("CREATE UNIQUE INDEX uq_tags_user_name_ci ON tags (user_id, LOWER(name))")
    
    op.create_table(
        'todo_tags',
        sa.Column('todo_id', sa.Uuid(), nullable=False),
        sa.Column('tag_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['todo_id'], ['todos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('todo_id', 'tag_id'),
    )
    op.create_index('ix_todo_tags_tag_id', 'todo_tags', ['tag_id'])
    op.create_index('ix_todo_tags_todo_id', 'todo_tags', ['todo_id'])

def downgrade() -> None:
    op.drop_table('todo_tags')
    op.execute("DROP INDEX IF EXISTS uq_tags_user_name_ci")
    op.drop_index('ix_tags_user_id', table_name='tags')
    op.drop_table('tags')
