"""add is_turkish_provider

Revision ID: 9f899fdf2569
Revises: 0d4c1ee4b97c
Create Date: 2024-06-18 15:55:45.154522

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '9f899fdf2569'
down_revision = '0d4c1ee4b97c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lastwatched', sa.Column('is_turkish_provider', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lastwatched', 'is_turkish_provider')
    # ### end Alembic commands ###