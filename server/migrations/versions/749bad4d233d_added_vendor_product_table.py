"""added vendor_product table

Revision ID: 749bad4d233d
Revises: 961377968cb6
Create Date: 2023-11-30 21:06:18.233620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '749bad4d233d'
down_revision = '961377968cb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vendor_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('delivery_cost', sa.Float(), nullable=True),
    sa.Column('mode_of_payment', sa.String(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id', 'vendor_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendor_products')
    # ### end Alembic commands ###
