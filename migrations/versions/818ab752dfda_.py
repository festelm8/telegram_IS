"""empty message

Revision ID: 818ab752dfda
Revises: 81e0c44fc0c7
Create Date: 2018-01-25 22:03:51.001679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '818ab752dfda'
down_revision = '81e0c44fc0c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('class_schedule', sa.Column('course_group_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint('class_schedule_course_number_id_fkey', 'class_schedule', type_='foreignkey')
    op.create_foreign_key('class_schedule_course_group_id_fkey', 'class_schedule', 'course_groups', ['course_group_id'], ['id'])
    op.drop_column('class_schedule', 'course_number_id')
    op.alter_column('course_groups', 'gid',
               existing_type=sa.INTEGER(),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True,
               autoincrement=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('course_groups', 'gid',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.INTEGER(),
               existing_nullable=True,
               autoincrement=False)
    op.add_column('class_schedule', sa.Column('course_number_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint('class_schedule_course_group_id_fkey', 'class_schedule', type_='foreignkey')
    op.create_foreign_key('class_schedule_course_number_id_fkey', 'class_schedule', 'course_numbers', ['course_number_id'], ['id'])
    op.drop_column('class_schedule', 'course_group_id')
    # ### end Alembic commands ###