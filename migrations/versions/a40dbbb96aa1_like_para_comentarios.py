"""Like para comentarios

Revision ID: a40dbbb96aa1
Revises: 
Create Date: 2023-08-31 14:24:22.450286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a40dbbb96aa1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comentarios_like',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comentario.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usuario.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comentarios_like')
    # ### end Alembic commands ###