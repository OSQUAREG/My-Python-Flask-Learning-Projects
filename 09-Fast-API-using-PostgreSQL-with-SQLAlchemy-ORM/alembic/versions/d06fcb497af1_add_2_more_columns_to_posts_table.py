"""add 2 more columns to posts table

Revision ID: d06fcb497af1
Revises: 6070e5d1c50e
Create Date: 2022-12-26 22:29:45.787034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd06fcb497af1'
down_revision = '6070e5d1c50e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="posts",
        column=sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)

    op.add_column(
        table_name="posts",
        column=sa.Column("created_on", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")), )
    pass


def downgrade() -> None:
    op.drop_column(
        table_name="posts",
        column_name="published")

    op.drop_column(
        table_name="posts",
        column_name="created_on")
    pass
