"""added thumbnail relationship. Renamed taxomomy -> taxonomy

Revision ID: 1f39c8e8d787
Revises: 62cf9338b8c6
Create Date: 2017-06-18 21:38:29.322967

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f39c8e8d787'
down_revision = '62cf9338b8c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('taxonomy', sa.String(length=300), nullable=True))
    op.drop_column('collection', 'taxomomy')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('taxomomy', mysql.VARCHAR(collation=u'utf8mb4_unicode_ci', length=300), nullable=True))
    op.drop_column('collection', 'taxonomy')
    # ### end Alembic commands ###
