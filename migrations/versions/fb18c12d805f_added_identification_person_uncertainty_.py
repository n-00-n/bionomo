"""added identification_person, uncertainty, authorship. removed aquisition_person from collection

Revision ID: fb18c12d805f
Revises: 33c76a0d8986
Create Date: 2017-06-14 11:00:26.773381

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fb18c12d805f'
down_revision = '33c76a0d8986'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('identification_person', sa.String(length=100), nullable=True))
    op.add_column('collection', sa.Column('taxomomy', sa.String(length=300), nullable=True))
    op.add_column('collection', sa.Column('uncertainty', sa.Integer(), nullable=True))
    op.drop_column('collection', 'aquisition_person')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('aquisition_person', mysql.VARCHAR(collation=u'utf8mb4_unicode_ci', length=100), nullable=True))
    op.drop_column('collection', 'uncertainty')
    op.drop_column('collection', 'taxomomy')
    op.drop_column('collection', 'identification_person')
    # ### end Alembic commands ###
