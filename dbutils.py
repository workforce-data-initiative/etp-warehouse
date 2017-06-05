import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)


class DbConnectionFactory(object):

    def build_conn_str(self, db_conf):
        return None

    def start_session(self, db_conf):
        return None


class PsqlDbConnectionFactory(DbConnectionFactory):
    db_type = "POSTGRESQL"

    def build_conn_str(self, db_conf):
        if db_conf is None:
            raise ValueError("Database connection info required")

        return "postgresql://{0}:{1}@{2}:{3}/{4}".format(db_conf['username'],
                                                         db_conf['password'],
                                                         db_conf['hostname'],
                                                         db_conf['port'],
                                                         db_conf['dbname'])

    def start_session(self, db_conf):
        logger.info("Starting connection session to database, type {0}".format(self.db_type))

        engine = create_engine(self.build_conn_str(db_conf))
        sessionmaker().configure(bind=engine)
        return Session()


class DbConnection(object):

    def __init__(self, db_conn, db_info):
        self.conn_session = db_conn.start_session(db_info)
