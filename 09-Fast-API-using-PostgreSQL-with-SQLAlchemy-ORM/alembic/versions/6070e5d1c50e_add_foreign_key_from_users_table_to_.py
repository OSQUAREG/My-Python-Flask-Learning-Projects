"""add foreign-key from users table to posts table

Revision ID: 6070e5d1c50e
Revises: de2e18bae53e
Create Date: 2022-12-26 20:45:13.860313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6070e5d1c50e'
down_revision = 'de2e18bae53e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="posts",
        column=sa.Column("author_id", sa.Integer(), nullable=False))

    op.create_foreign_key(
        constraint_name="posts_users_fk",
        source_table="posts",  # the table where your fkey is added
        referent_table="users",  # the table giving the fkey
        local_cols=["author_id"],  # the column where your fkey is added.
        remote_cols=["id"],  # the column giving the fkey that is used.
        ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="posts_users_fk",
        table_name="posts")

    op.drop_column(
        table_name="posts",
        column_name="author_id")
    pass
