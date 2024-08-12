import ast
import logging
import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DEFAULT_DB_SCHEMA_NAME = "k3tog"

metadata_obj = MetaData(schema=os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME))

Base = declarative_base(metadata_obj)


def _get_db_config_dict():
    return {
        "db_username": os.environ.get("DB_USERNAME", "k3tog_api_user"),
        "db_password": os.environ.get("DB_PASSWORD", "password"),
        "db_host": os.environ.get("DB_HOST", "localhost"),
        "db_port": int(os.environ.get("DB_PORT", "15432")),
        "db_name": os.environ.get("DB_NAME", "k3tog_dev_db"),
        "search_path": metadata_obj.schema,
    }


def get_connection_string():
    config_dict = _get_db_config_dict()
    return (
        "postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        "?options=-csearch_path={search_path}".format(**config_dict)
    )


def get_engine():
    logger.debug("[DB] creating new engine")

    return create_engine(
        get_connection_string(),
        pool_size=int(os.environ.get("DB_POOL_SIZE", "10")),
        max_overflow=int(
            os.environ.get("DB_POOL_MAX_OVERFLOW", "3"),
        ),
        echo=ast.literal_eval(os.environ.get("DB_ENABLE_ENGINE_ECHO", "False")),
        connect_args={},
    )


default_engine = get_engine()
default_sessionmaker = sessionmaker(bind=default_engine)


def _get_db_session(engine=None):
    session_cls = sessionmaker(bind=engine) if engine else default_sessionmaker
    return session_cls()


def get_db_session(engine=None):
    return _get_db_session()
