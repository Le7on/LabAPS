"""add staff-project qualification association

Adds the Staff<->Project many-to-many link (staff_project): which projects a
staff member is qualified for (ADR-014).

Revision ID: a1c2e3f40506
Revises: 2d71eedd0842
Create Date: 2026-07-10 22:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c2e3f40506'
down_revision: Union[str, Sequence[str], None] = '2d71eedd0842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'staff_project',
        sa.Column('staff_id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['staff_id'], ['staff.id']),
        sa.ForeignKeyConstraint(['project_id'], ['project.id']),
        sa.PrimaryKeyConstraint('staff_id', 'project_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('staff_project')
