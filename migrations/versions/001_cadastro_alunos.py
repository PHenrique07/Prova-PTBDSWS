"""Cria as tabelas de disciplinas e alunos.

Revision ID: 001_cadastro_alunos
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = '001_cadastro_alunos'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'disciplinas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=5), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
    )
    op.create_table(
        'alunos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=64), nullable=False),
        sa.Column('disciplina_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('alunos')
    op.drop_table('disciplinas')
