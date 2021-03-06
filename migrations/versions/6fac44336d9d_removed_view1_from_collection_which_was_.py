"""removed view1 from collection (which was just for testing). added technical_contact_email to Provider

Revision ID: 6fac44336d9d
Revises: 30ebb0795a99
Create Date: 2017-06-03 21:41:29.424844

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6fac44336d9d'
down_revision = '30ebb0795a99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('collection', 'views_1')
    op.add_column('provider', sa.Column('technical_contact_phone', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('provider', 'technical_contact_phone')
    op.add_column('collection', sa.Column('views_1', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
