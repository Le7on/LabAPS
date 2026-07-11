"""add calendar fields to plan and assignment

Adds plan calendar configuration (start_date, end_date, shift_mode,
skipped_dates) and assignment real-calendar times (planned_start_at,
planned_end_at, planned_shift) for integer-unit -> shift-calendar mapping
(ADR-016).

Revision ID: c3e4a5162839
Revises: b2d3f5061728
Create Date: 2026-07-11 00:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e4a5162839'
down_revision: Union[str, Sequence[str], None] = 'b2d3f5061728'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('plan', sa.Column('start_date', sa.String(length=10), nullable=True))
    op.add_column('plan', sa.Column('end_date', sa.String(length=10), nullable=True))
    op.add_column(
        'plan',
        sa.Column('shift_mode', sa.String(length=10), nullable=False, server_default='single'),
    )
    op.add_column(
        'plan',
        sa.Column('skipped_dates', sa.JSON(), nullable=False, server_default='[]'),
    )

    op.add_column(
        'assignment', sa.Column('planned_start_at', sa.String(length=25), nullable=True)
    )
    op.add_column(
        'assignment', sa.Column('planned_end_at', sa.String(length=25), nullable=True)
    )
    op.add_column('assignment', sa.Column('planned_shift', sa.String(length=20), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('assignment', 'planned_shift')
    op.drop_column('assignment', 'planned_end_at')
    op.drop_column('assignment', 'planned_start_at')
    op.drop_column('plan', 'skipped_dates')
    op.drop_column('plan', 'shift_mode')
    op.drop_column('plan', 'end_date')
    op.drop_column('plan', 'start_date')
