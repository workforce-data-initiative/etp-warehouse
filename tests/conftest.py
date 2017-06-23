import os
import pytest
from alembic import config

from dbutils import conn_uri_factory


def pytest_addoption(parser):
    """
    Custom command line options required for test runs
    """

    parser.addoption('--name', action='store', default=None,
                     help='Name of schema to operate on i.e transactional | warehouse')
    parser.addoption('--adapter', action='store', default='sqlite',
                     help='SQLAlchemy database connection adapter')
    parser.addoption('--conf', action='store',
                     default=os.path.join(os.path.dirname(__file__), '../alembic.ini'),
                     help="Alembic config INI path")
    parser.addoption('--dbconf', action='store',
                     default=os.path.join(os.path.dirname(__file__), '../conf/dbconf_dev.yml'),
                     help='Database connection parameters YAML path')


@pytest.fixture(scope='session')
def alchemy_url(request):
    return conn_uri_factory(request.config.getoption('--dbconf'),
                            request.config.getoption('--adapter'))


@pytest.fixture(scope='session')
def alembic_cfg(request):
    return request.config.getoption('--conf')


@pytest.fixture(scope='session')
def schema_name(request):
    return request.config.getoption('--name')


@pytest.fixture(scope='session')
def db_setup(alembic_cfg, schema_name):
    # run all db migrations
    config.main(['-c', alembic_cfg, '-n', schema_name, 'upgrade', 'head'])
