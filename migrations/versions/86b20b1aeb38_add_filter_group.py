"""add filter_group

Revision ID: 86b20b1aeb38
Revises: cfce02eb9b5a
Create Date: 2023-08-06 21:19:03.222701

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = '86b20b1aeb38'
down_revision = 'cfce02eb9b5a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filtergroup',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('ordered_filter_ids_str', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('filtergroup', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_filtergroup_id'), ['id'], unique=False)

    op.create_table('filterfiltergrouplink',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('filter_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('filter_group_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['filter_group_id'], ['filtergroup.id'], ),
    sa.ForeignKeyConstraint(['filter_id'], ['filter.id'], ),
    sa.PrimaryKeyConstraint('filter_id', 'filter_group_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('filterfiltergrouplink')
    with op.batch_alter_table('filtergroup', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_filtergroup_id'))

    op.drop_table('filtergroup')
    # ### end Alembic commands ###
