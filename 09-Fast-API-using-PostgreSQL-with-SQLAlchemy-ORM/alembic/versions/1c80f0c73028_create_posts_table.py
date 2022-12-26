"""create posts table

Revision ID: 1c80f0c73028
Revises: 
Create Date: 2022-12-26 18:27:35.382854

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1c80f0c73028'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table(table_name="posts")
    pass
