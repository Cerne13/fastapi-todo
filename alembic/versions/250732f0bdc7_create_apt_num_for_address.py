"""create apt_num for address

Revision ID: 250732f0bdc7
Revises: d2c54d8ce3a6
Create Date: 2023-04-02 11:59:13.665616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '250732f0bdc7'
down_revision = 'd2c54d8ce3a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
