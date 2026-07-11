"""equipment applicable-projects and drop capabilities

ADR-018: Equipment declares applicable projects (equipment_project) and binds
methods (method_equipment, already present). The unused capabilities column is
removed.

Revision ID: e5061728a9bc
Revises: d4f5061728a9
Create Date: 2026-07-11 02:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5061728a9bc'
down_revision: Union[str, Sequence[str], None] = 'd4f5061728a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'equipment_project',
        sa.Column('equipment_id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id']),
        sa.ForeignKeyConstraint(['project_id'], ['project.id']),
        sa.PrimaryKeyConstraint('equipment_id', 'project_id'),
    )
    op.drop_column('equipment', 'capabilities')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'equipment',
        sa.Column('capabilities', sa.JSON(), nullable=False, server_default='[]'),
    )
    op.drop_table('equipment_project')
