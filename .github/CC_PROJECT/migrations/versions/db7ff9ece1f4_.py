"""empty message

Revision ID: db7ff9ece1f4
Revises: 
Create Date: 2025-03-22 17:08:54.947351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7ff9ece1f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('max_participants',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=200),
               existing_nullable=True)

    with op.batch_alter_table('registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registration_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('registered_at')
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), nullable=True))
        batch_op.add_column(sa.Column('registered_at', sa.DATETIME(), nullable=True))
        batch_op.drop_column('registration_date')

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
        batch_op.alter_column('max_participants',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.drop_column('category')

    # ### end Alembic commands ###
