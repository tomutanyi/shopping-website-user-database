"""added dict to products

Revision ID: ff8e05fd3182
Revises: 9930888701be
Create Date: 2023-11-30 18:32:34.676605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8e05fd3182'
down_revision = '9930888701be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('search_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('search_history', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###
