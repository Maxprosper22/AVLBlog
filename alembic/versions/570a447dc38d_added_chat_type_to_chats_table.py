"""Added chat type to chats table

Revision ID: 570a447dc38d
Revises: ec05c6e75eed
Create Date: 2022-11-10 09:08:43.936785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '570a447dc38d'
down_revision = 'ec05c6e75eed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('chat_type', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'chat_type')
    # ### end Alembic commands ###
