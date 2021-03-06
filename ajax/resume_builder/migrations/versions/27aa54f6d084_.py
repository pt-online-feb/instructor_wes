"""empty message

Revision ID: 27aa54f6d084
Revises: a713da7e7cf5
Create Date: 2019-03-25 17:48:43.243406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27aa54f6d084'
down_revision = 'a713da7e7cf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=45), nullable=False, server_default="Test"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume_items', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
