"""create users table

Revision ID: de2e18bae53e
Revises: de02967918cd
Create Date: 2022-12-26 20:24:05.428341

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'de2e18bae53e'
down_revision = 'de02967918cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_on", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),  # sets the column with primary key constraint
        sa.UniqueConstraint("email")  # sets the column with the unique constraint.
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
