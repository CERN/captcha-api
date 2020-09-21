"""Add captcha table

Revision ID: ddca5caebdd6
Revises:
Create Date: 2020-09-18 17:47:11.382882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ddca5caebdd6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "captcha",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("answer", sa.String(length=120), nullable=False),
        sa.Column("creation_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("captcha")
