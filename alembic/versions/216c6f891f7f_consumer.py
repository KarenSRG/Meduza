"""consumer

Revision ID: 216c6f891f7f
Revises: 3c9382fd9472
Create Date: 2024-08-16 17:25:47.975558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '216c6f891f7f'
down_revision: Union[str, None] = '3c9382fd9472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### consumer_commands auto generated by Alembic - please adjust! ###
    op.create_table('consumers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('current_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consumers_id'), 'consumers', ['id'], unique=True)
    # ### end Alembic consumer_commands ###


def downgrade() -> None:
    # ### consumer_commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_consumers_id'), table_name='consumers')
    op.drop_table('consumers')
    # ### end Alembic consumer_commands ###
