"""create transactional database and tables from scratch

Revision ID: ca392f163b2f
Revises: 045af34660d0
Create Date: 2017-06-15 21:36:50.379042

"""
import os
from alembic import context, command
from alembic.config import Config

from models.transactional import Base


# revision identifiers, used by Alembic.
revision = 'ca392f163b2f'
down_revision = None
branch_labels = None
depends_on = None

# load the Alembic configuration
alembic_ini = os.path.join(os.path.dirname(__file__), '../../', 'alembic.ini')
migration_context = context.get_context()


# add schemas
def upgrade():
    conn = migration_context.bind

    with conn.begin() as transaction:
        Base.metadata.create_all(conn)

        # generate the version table, "stamping" it with the most recent rev:
        # command.stamp(Config(alembic_ini), 'head')


def downgrade():
    pass
