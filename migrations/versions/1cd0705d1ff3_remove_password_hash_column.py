"""remove password_hash column

Revision ID: 1cd0705d1ff3
Revises: 47ac7b97249f
Create Date: 2023-11-08 23:23:37.224835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1cd0705d1ff3'
down_revision = '47ac7b97249f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False))

    # ### end Alembic commands ###
