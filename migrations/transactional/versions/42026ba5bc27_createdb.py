"""createdb

Revision ID: 42026ba5bc27
Revises: 
Create Date: 2017-06-22 20:07:58.548427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42026ba5bc27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('entity_type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_table('exit_type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_table('outcome',
    sa.Column('potential_outcome_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('potential_outcome_id')
    )
    op.create_table('participant',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('wioa_participant', sa.Boolean(), nullable=False),
    sa.Column('wioa_lta_participant', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('participant_id')
    )
    op.create_table('program',
    sa.Column('program_cip', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('potential_outcome_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['potential_outcome_id'], ['outcome.potential_outcome_id'], ),
    sa.PrimaryKeyConstraint('program_cip')
    )
    op.create_table('provider',
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['entity_type.type_id'], ),
    sa.PrimaryKeyConstraint('provider_id')
    )
    op.create_table('wage',
    sa.Column('wage_start_date', sa.Date(), nullable=False),
    sa.Column('wage_end_date', sa.Date(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('wage_amt', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.PrimaryKeyConstraint('wage_start_date', 'wage_end_date', 'participant_id')
    )
    op.create_table('participant_program',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('program_cip', sa.Integer(), nullable=False),
    sa.Column('entry_date', sa.Date(), nullable=False),
    sa.Column('exit_date', sa.Date(), nullable=True),
    sa.Column('enrolled', sa.Boolean(), nullable=False),
    sa.Column('exit_type_id', sa.Integer(), nullable=True),
    sa.Column('obtained_credential', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['exit_type_id'], ['exit_type.type_id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.ForeignKeyConstraint(['program_cip'], ['program.program_cip'], ),
    sa.PrimaryKeyConstraint('participant_id', 'program_cip')
    )
    op.create_table('program_provider',
    sa.Column('program_cip', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['program_cip'], ['program.program_cip'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.provider_id'], ),
    sa.PrimaryKeyConstraint('program_cip', 'provider_id')
    )


def downgrade():
    op.drop_table('program_provider')
    op.drop_table('participant_program')
    op.drop_table('wage')
    op.drop_table('provider')
    op.drop_table('program')
    op.drop_table('participant')
    op.drop_table('outcome')
    op.drop_table('exit_type')
    op.drop_table('entity_type')
