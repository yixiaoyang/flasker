"""empty message

Revision ID: f5d17540f4f
Revises: None
Create Date: 2015-11-09 19:34:22.962362

"""

# revision identifiers, used by Alembic.
revision = 'f5d17540f4f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('content', sa.String(length=64), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    ### end Alembic commands ###