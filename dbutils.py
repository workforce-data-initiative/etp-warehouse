import logging
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)


class DbConfValidator(object):

    @staticmethod
    def validate_conf(db_conf):
        pass


class DbConnectionUri(object):

    @classmethod
    def build_conn_uri(cls, db_conf):
        pass


class SqliteDbConfValidator(DbConfValidator):

    @staticmethod
    def validate_conf(db_conf):
        """
        Validate SQLite database connection parameters

        :param db_conf: dict of connection parameters
        :return: dict of validate connection parameters
        """

        logger.info("Validating database connection configs")

        if db_conf is None:
            raise ValueError("Database connection configs required")

        return db_conf


class PsqlDbConfValidator(DbConfValidator):

    @staticmethod
    def validate_conf(db_conf):
        """
        Validate PostgreSQL database connection parameters

        :param db_conf: dict of connection parameters
        :return: dict of validate connection parameters
        """

        logger.info("Validating database connection configs")

        if db_conf is None:
            raise ValueError("Database connection configs required")

        return db_conf


class SqliteDbConnectionUri(DbConnectionUri):

    db_adapter = "sqlite"
    conn_uri = "{db_adapter}:///{db_path}"

    @classmethod
    def build_conn_uri(cls, db_conf):
        """
        Create database connection uri for SQLite

        :param db_conf: dict of connection parameters
        :return: valid connection string for database built
                from parameters passed in db_conf
        """

        db_conf = SqliteDbConfValidator.validate_conf(db_conf)

        return cls.conn_uri.format(db_adapter=cls.db_adapter, db_path=db_conf['database'])


class PsqlDbConnectionUri(DbConnectionUri):

    db_adapter = "postgresql"
    conn_uri = "{db_adapter}://{username}:{password}@{host}:{port}/{database}"

    @classmethod
    def build_conn_uri(cls, db_conf):
        """
        Create database connection uri for PostgreSQL

        :param db_conf: dict of connection parameters
        :return: valid connection string for database built
                from parameters passed in db_conf
        """

        db_conf = PsqlDbConfValidator.validate_conf(db_conf)

        return cls.conn_uri.format(db_adapter=cls.db_adapter, username=db_conf['username'],
                                    password=db_conf['password'], host=db_conf['host'],
                                    port=db_conf['port'], database=db_conf['database'])


class DbConnection(object):
    Session = sessionmaker()

    def __init__(self, conn_uri):
        self.engine = create_engine(conn_uri)

    def start_session(self):
        """
        Start database connection session

        :return: new session object bound to instance engine created from
                connection string passed on DbConnection object creation
        """

        logger.info("Starting database connection session")

        self.Session.configure(bind=self.engine)
        return Session()


# selector for supported database connections
db_uris = {'sqlite': SqliteDbConnectionUri().__class__,
           'postgresql': PsqlDbConnectionUri().__class__}


def read_dbconf(conf_file, db_adapter):
    """
    Read (yaml format) database configuration file

    :param conf_file: YAML file containing database connection params
    :param db_adapter: Database adapter name
    :raises: TypeError, when conf_file or db_adapter passed is None
             FileNotFoundError if conf_file is not found or yaml.YAMLError
             if conf_file yaml is not read
    :return: dict of database conf for the specified db_adapter
    """

    try:
        with open(conf_file, 'r') as yml_conf:
            conf = yaml.load(yml_conf)
    except(TypeError, FileNotFoundError, yaml.YAMLError) as err:
        logger.debug(err)
        raise

    return conf.get(db_adapter)


def conn_uri_factory(conf_file, db_adapter):
    """
    Create the applicable connection uri for the database adapter
    passed using parameters read from config file

    :param conf_file: YAML file containing database connection params
                      used by SQLAlchemy to create connection. Supported
                      fields include SQLAlchemy database adapter name, host
                      port, username, password, database
    :param db_adapter: Database adapter name as accepted by SQLAlchemy
    :return: SQLAlchemy connection uri for the database with specified adapter
    """

    try:
        db_conf = read_dbconf(conf_file, db_adapter)
    except Exception as err:
        logger.debug(err)
        raise

    # dynamically select connection uri class
    UriClass = db_uris.get(db_adapter)
    return UriClass().build_conn_uri(db_conf)


# db inspector


