"""add playlist_item.duration

Revision ID: cfce02eb9b5a
Revises: 11e142e18c14
Create Date: 2023-08-05 15:45:46.723380

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'cfce02eb9b5a'
down_revision = '11e142e18c14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlistitem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('duration', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlistitem', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('duration')

    # ### end Alembic commands ###
