"""add shift, method-equipment, workflow project, gelatin type

Adds the Shift master data table, the Method<->Equipment binding
(method_equipment), workflow_definition.project_id, and
operation_definition.gelatin_type (ADR-015).

Revision ID: b2d3f5061728
Revises: a1c2e3f40506
Create Date: 2026-07-10 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d3f5061728'
down_revision: Union[str, Sequence[str], None] = 'a1c2e3f40506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'shift',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('shift_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('start_time', sa.String(length=5), nullable=False, server_default=''),
        sa.Column('end_time', sa.String(length=5), nullable=False, server_default=''),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=100), nullable=False, server_default='system'),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('updated_by', sa.String(length=100), nullable=False, server_default='system'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_shift_shift_code', 'shift', ['shift_code'])

    op.add_column(
        'workflow_definition',
        sa.Column('project_id', sa.String(length=36), nullable=False, server_default=''),
    )
    op.create_index(
        'ix_workflow_definition_project_id', 'workflow_definition', ['project_id']
    )

    op.add_column(
        'operation_definition',
        sa.Column('gelatin_type', sa.String(length=100), nullable=True),
    )

    op.add_column(
        'operation_instance',
        sa.Column('equipment_ids', sa.JSON(), nullable=False, server_default='[]'),
    )

    op.create_table(
        'method_equipment',
        sa.Column('operation_definition_id', sa.String(length=36), nullable=False),
        sa.Column('equipment_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['operation_definition_id'], ['operation_definition.id']),
        sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id']),
        sa.PrimaryKeyConstraint('operation_definition_id', 'equipment_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('method_equipment')
    op.drop_column('operation_instance', 'equipment_ids')
    op.drop_column('operation_definition', 'gelatin_type')
    op.drop_index('ix_workflow_definition_project_id', table_name='workflow_definition')
    op.drop_column('workflow_definition', 'project_id')
    op.drop_index('ix_shift_shift_code', table_name='shift')
    op.drop_table('shift')
