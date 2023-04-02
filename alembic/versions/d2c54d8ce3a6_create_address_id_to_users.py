"""create address_id to users

Revision ID: d2c54d8ce3a6
Revises: 4dd625b27f36
Create Date: 2023-04-01 21:32:16.585696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2c54d8ce3a6'
down_revision = '4dd625b27f36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'address_users_fk',
        source_table='users',
        referent_table='address',
        local_cols=['address_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users', 'address_id')
