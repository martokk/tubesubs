"""add video.view_count

Revision ID: d306d0ab74fd
Revises: 8218d280afd3
Create Date: 2023-08-09 23:09:53.326813

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # added


# revision identifiers, used by Alembic.
revision = "d306d0ab74fd"
down_revision = "8218d280afd3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("video", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("view_count", sa.Integer(), nullable=False, server_default="0")
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("video", schema=None) as batch_op:
        batch_op.drop_column("view_count")

    # ### end Alembic commands ###