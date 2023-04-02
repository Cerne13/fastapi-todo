"""create phone num for user col

Revision ID: 2e8da5ac3e4c
Revises: 
Create Date: 2023-04-01 17:41:27.814467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e8da5ac3e4c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
