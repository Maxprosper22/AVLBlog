"""added visibility field to chat table

Revision ID: 557798694c53
Revises: 13731d3842f7
Create Date: 2022-11-19 14:31:01.749224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '557798694c53'
down_revision = '13731d3842f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('visibility', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'visibility')
    # ### end Alembic commands ###