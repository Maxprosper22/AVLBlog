"""added chatname and removed nullable  argument in chats table

Revision ID: 638bef63ddab
Revises: ed7d38cd6c49
Create Date: 2022-11-11 19:21:41.019102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '638bef63ddab'
down_revision = 'ed7d38cd6c49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('chat_name', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'chat_name')
    # ### end Alembic commands ###
