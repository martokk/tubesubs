"""added thumbnail to playlist_item

Revision ID: f66306890361
Revises: f979187c6b80
Create Date: 2023-07-31 18:00:29.954022

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'f66306890361'
down_revision = 'f979187c6b80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlistitem', sa.Column('thumbnail', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('playlistitem', 'thumbnail')
    # ### end Alembic commands ###
