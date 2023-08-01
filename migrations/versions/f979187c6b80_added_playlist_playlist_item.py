"""added playlist & playlist_item

Revision ID: f979187c6b80
Revises: d6d0658d2a12
Create Date: 2023-07-31 16:17:51.720323

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'f979187c6b80'
down_revision = 'd6d0658d2a12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playlistitem',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('playlist_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlist.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url', 'playlist_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlistitem')
    op.drop_table('playlist')
    # ### end Alembic commands ###