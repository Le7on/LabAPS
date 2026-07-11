"""merge staff skill into project qualification and remove shift master data

ADR-017: Staff competency is a single set of qualified projects. Removes
Staff.skills / Staff.qualifications, drops the unused Shift master-data table,
drops method required_capability/skill/qualification columns, and adds
operation_instance.required_project_id (the workflow project used for staff
eligibility).

Revision ID: d4f5061728a9
Revises: c3e4a5162839
Create Date: 2026-07-11 01:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f5061728a9'
down_revision: Union[str, Sequence[str], None] = 'c3e4a5162839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Staff: drop free-text skills and qualifications (competency is now the
    # staff_project qualification link only).
    op.drop_column('staff', 'skills')
    op.drop_column('staff', 'qualifications')

    # Method definition: equipment binding (ADR-015) and project-based staff
    # eligibility (ADR-017) replace these string matches.
    op.drop_column('operation_definition', 'required_capability')
    op.drop_column('operation_definition', 'required_skill')
    op.drop_column('operation_definition', 'required_qualification')

    # Operation instance: same removals, plus the workflow project for staff
    # eligibility.
    op.drop_column('operation_instance', 'required_capability')
    op.drop_column('operation_instance', 'required_skill')
    op.drop_column('operation_instance', 'required_qualification')
    op.add_column(
        'operation_instance',
        sa.Column('required_project_id', sa.String(length=36), nullable=True),
    )

    # Remove the unused Shift master-data table.
    op.drop_index('ix_shift_shift_code', table_name='shift')
    op.drop_table('shift')


def downgrade() -> None:
    """Downgrade schema."""
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

    op.drop_column('operation_instance', 'required_project_id')
    op.add_column(
        'operation_instance',
        sa.Column('required_qualification', sa.String(length=100), nullable=True),
    )
    op.add_column(
        'operation_instance', sa.Column('required_skill', sa.String(length=100), nullable=True)
    )
    op.add_column(
        'operation_instance',
        sa.Column('required_capability', sa.String(length=100), nullable=True),
    )

    op.add_column(
        'operation_definition',
        sa.Column('required_qualification', sa.String(length=100), nullable=True),
    )
    op.add_column(
        'operation_definition', sa.Column('required_skill', sa.String(length=100), nullable=True)
    )
    op.add_column(
        'operation_definition',
        sa.Column('required_capability', sa.String(length=100), nullable=True),
    )

    op.add_column('staff', sa.Column('qualifications', sa.JSON(), nullable=False, server_default='{}'))
    op.add_column('staff', sa.Column('skills', sa.JSON(), nullable=False, server_default='[]'))
