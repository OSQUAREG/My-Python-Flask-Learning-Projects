"""add content column

Revision ID: de02967918cd
Revises: 1c80f0c73028
Create Date: 2022-12-26 19:34:53.936738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de02967918cd'
down_revision = '1c80f0c73028'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="posts",
        column=sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
