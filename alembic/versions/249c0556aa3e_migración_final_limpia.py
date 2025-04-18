"""Migración final limpia

Revision ID: 249c0556aa3e
Revises: 
Create Date: 2025-04-18 16:01:19.026102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '249c0556aa3e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('provider', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('horas_contrato', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('total_hours', sa.String(), nullable=False),
    sa.Column('total_hr_hours', sa.String(), nullable=False),
    sa.Column('complementary_hours', sa.String(), nullable=False),
    sa.Column('total_festive_hours', sa.String(), nullable=False),
    sa.Column('total_sunday_hours', sa.String(), nullable=False),
    sa.Column('total_early_days', sa.Integer(), nullable=False),
    sa.Column('total_night_hours', sa.String(), nullable=False),
    sa.Column('total_meal_allowance', sa.Integer(), nullable=False),
    sa.Column('total_split_shifts', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reports_id'), 'reports', ['id'], unique=False)
    op.create_table('day_summaries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.String(), nullable=False),
    sa.Column('duracion_total', sa.String(), nullable=False),
    sa.Column('horas_perentorias', sa.String(), nullable=False),
    sa.Column('festive_hours', sa.String(), nullable=False),
    sa.Column('horas_domingos', sa.String(), nullable=False),
    sa.Column('horas_madrugue', sa.String(), nullable=False),
    sa.Column('horas_nocturnas', sa.String(), nullable=False),
    sa.Column('manutencion', sa.Integer(), nullable=False),
    sa.Column('fraccionadas', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_day_summaries_id'), 'day_summaries', ['id'], unique=False)
    op.create_table('shifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('hora_entrada', sa.String(), nullable=False),
    sa.Column('hora_salida', sa.String(), nullable=False),
    sa.Column('tipo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['day_summaries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shifts_id'), 'shifts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shifts_id'), table_name='shifts')
    op.drop_table('shifts')
    op.drop_index(op.f('ix_day_summaries_id'), table_name='day_summaries')
    op.drop_table('day_summaries')
    op.drop_index(op.f('ix_reports_id'), table_name='reports')
    op.drop_table('reports')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
