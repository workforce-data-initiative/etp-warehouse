from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine
from logging.config import fileConfig
import logging

from models.transactional import Base
from dbutils import conn_uri_factory

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

args = context.get_x_argument(as_dictionary=True)


def usage():
    usage_str = "Usage: alembic [-c CONFIG] -n SCHEMA NAME " \
                "[--adapter=SQLALCHEMY ADAPTER ][--dbconf=DB (YAML) CONFIG]"
    eg_str = "       alembic -c alembic.ini -n schema1 " \
             "--adapter=sqlite --dbconf=conf/db.conf"
    return "{0}\n{1}".format(usage_str, eg_str)


def conn_url():
    print(config.get_main_option("default_dbconf"))

    try:
        url = conn_uri_factory(args.get("dbconf", config.get_main_option("default_dbconf")),
                               args.get("adapter", config.get_main_option("default_adapter")))
    except Exception as err:
        logger.debug(err)
        raise

    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    context.configure(
        url=conn_url(), target_metadata=target_metadata,
        transactional_ddl=True, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = create_engine(conn_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transactional_ddl=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
