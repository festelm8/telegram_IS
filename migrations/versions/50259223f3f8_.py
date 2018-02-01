"""empty message

Revision ID: 50259223f3f8
Revises: 2b7fdc269df5
Create Date: 2018-01-31 19:42:17.238070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50259223f3f8'
down_revision = '2b7fdc269df5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
