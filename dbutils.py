import logging
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)


def get_dbconf(conf_file, db_adapter):

    conf = None

    try:
        with open(conf_file, 'r') as yml_conf:
            conf = yaml.load(yml_conf)
    except FileNotFoundError as err:
        logger.debug(err)

    for db_conf in conf:
        if db_conf == db_adapter:
            return db_conf


class DbConfValidator(object):

    @staticmethod
    def validate_conf(db_conf):
        pass


class SqliteDbConfValidator(DbConfValidator):
    pass


class PsqlDbConfValidator(DbConfValidator):

    @staticmethod
    def validate_conf(db_conf):
        logger.info("Validating database connection configs")

        if db_conf is None:
            raise ValueError("Database connection configs required")


class DbConnectionUri(object):

    @classmethod
    def build_conn_uri(cls, db_conf):
        pass


class SqliteDbConnectionUri(DbConnectionUri):

    db_adapter = "sqlite"
    conn_uri = "{db_adapter}:///{db_path}"

    @classmethod
    def build_conn_uri(cls, db_conf):
        db_conf = SqliteDbConfValidator.validate_conf(db_conf)

        return cls.conn_uri.format(db_adapter=cls.db_adapter, db_path=db_conf['database'])


class PsqlDbConnectionUri(DbConnectionUri):

    db_adapter = "postgresql"
    conn_uri = "{db_adapter}://{username}:{password}@{host}:{port}/{database}"

    @classmethod
    def build_conn_uri(cls, db_conf):
        db_conf = PsqlDbConfValidator.validate_conf(db_conf)

        return cls.conn_uri.format(db_adapter=cls.db_adapter, username=db_conf['username'],
                                    password=db_conf['password'], host=db_conf['host'],
                                    port=db_conf['port'], database=db_conf['database'])


class DbConnection(object):
    Session = sessionmaker()

    def __init__(self, conn_uri):
        self.engine = create_engine(conn_uri)

    def start_session(self):
        logger.info("Starting database connection session")

        self.Session.configure(bind=self.engine)
        return Session()

# db inspector
