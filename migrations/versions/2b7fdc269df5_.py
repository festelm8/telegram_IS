"""empty message

Revision ID: 2b7fdc269df5
Revises: 818ab752dfda
Create Date: 2018-01-31 19:18:08.248280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b7fdc269df5'
down_revision = '818ab752dfda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('class_schedule', sa.Column('seq', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('class_schedule', 'seq')
    # ### end Alembic commands ###