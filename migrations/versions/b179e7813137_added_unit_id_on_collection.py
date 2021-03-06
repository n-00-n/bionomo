"""added unit_id on collection

Revision ID: b179e7813137
Revises: 23ee12e1be41
Create Date: 2017-05-22 08:52:39.532944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b179e7813137'
down_revision = '23ee12e1be41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('unit_id', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('collection', 'unit_id')
    # ### end Alembic commands ###
