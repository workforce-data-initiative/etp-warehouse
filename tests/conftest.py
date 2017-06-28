import os
import pytest
from sqlalchemy.inspection import inspect
from sqlalchemy_utils.functions import drop_database
from alembic import config

from dbutils import conn_uri_factory, DbConnection


def pytest_addoption(parser):
    """
    Custom command line options required for test runs
    """

    parser.addoption('--name', action='store', default=None,
                     help='Schema [transactional | warehouse] to operate on')
    parser.addoption('--adapter', action='store', default='sqlite',
                     help='SQLAlchemy database connection adapter')
    parser.addoption('--conf', action='store',
                     default=os.path.join(os.path.dirname(__file__),
                                          '../alembic.ini'),
                     help="Alembic config INI path")
    parser.addoption('--dbconf', action='store',
                     default=os.path.join(os.path.dirname(__file__),
                                          '../conf/db.yml'),
                     help='Database connection parameters YAML path')


@pytest.fixture(scope='session')
def schema_name(request):
    return request.config.getoption('--name')


@pytest.fixture(scope='session')
def alembic_cfg(request):
    return request.config.getoption('--conf')


@pytest.fixture(scope='session')
def db_conf(request):
    return request.config.getoption('--dbconf')


@pytest.fixture(scope='session')
def db_adapter(request):
    return request.config.getoption('--adapter')


@pytest.fixture(scope='session')
def alchemy_url(db_conf, db_adapter, schema_name, request):
    return conn_uri_factory(db_conf, db_adapter, schema_name)


@pytest.fixture(scope='session', autouse=True)
def db_setup(alembic_cfg, schema_name, db_conf, db_adapter, alchemy_url, request):
    # run all db migrations
    config.main(['-c', alembic_cfg, '-n', schema_name,
                 '-x', 'dbconf={0}'.format(db_conf),
                 '-x', 'adapter={0}'.format(db_adapter),
                 'upgrade', 'head'])

    def db_drop():
        # db teardown - drop all
        config.main(['-c', alembic_cfg, '-n', schema_name,
                     '-x', 'dbconf={0}'.format(db_conf),
                     '-x', 'adapter={0}'.format(db_adapter),
                     'downgrade', 'base'])
        # drop db incl. alembic tables
        drop_database(alchemy_url)

    request.addfinalizer(db_drop)


@pytest.fixture(scope='session')
def db_conn(alchemy_url):
    return DbConnection(alchemy_url)


@pytest.fixture(scope='session')
def db_inspector(db_conn):
    return inspect(db_conn.engine)


@pytest.fixture(scope='session')
def alembic_tables():
    """
    Tables created by Alembic to track migrations.
    Fixture is maintained to differentiate alembic tables
    from application tables when `inspector.get_table_names()`
    for tests
    """

    tbl_list = ['alembic_version']
    return tbl_list


@pytest.fixture(scope='session')
def db_tables(schema_name):
    """
    Manifest of all application tables expected
    in database when all migrations are run
    """

    if schema_name.lower() == 'transactional':
        tbl_list = ['participant', 'program',
                    'participant_program', 'program_provider',
                    'provider', 'outcome',
                    'exit_type', 'wage', 'entity_type']
    else:
        tbl_list = []

    # sort table list - easier test comparison
    tbl_list.sort()

    return tbl_list
