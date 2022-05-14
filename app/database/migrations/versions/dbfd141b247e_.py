"""empty message

Revision ID: dbfd141b247e
Revises: 
Create Date: 2022-04-24 13:28:43.377596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfd141b247e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comix',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('autor', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comix')
    # ### end Alembic commands ###