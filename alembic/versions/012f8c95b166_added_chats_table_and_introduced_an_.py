"""Added chats table and introduced an association table to associate users and chats

Revision ID: 012f8c95b166
Revises: 
Create Date: 2022-11-10 08:35:14.066073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012f8c95b166'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('chat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'messages', 'chats', ['chat_id'], ['chat_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'chat_id')
    # ### end Alembic commands ###
