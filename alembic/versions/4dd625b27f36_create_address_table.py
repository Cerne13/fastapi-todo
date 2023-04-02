"""create address table

Revision ID: 4dd625b27f36
Revises: 2e8da5ac3e4c
Create Date: 2023-04-01 17:56:46.449399

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4dd625b27f36'
down_revision = '2e8da5ac3e4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postal_code', sa.String(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('address')
