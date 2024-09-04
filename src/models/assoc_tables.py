import logging
import os

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func, Float
from db.database import DEFAULT_DB_SCHEMA_NAME, Base


logger = logging.getLogger(__name__)

project_id = f"{os.environ.get('DB_SCHEMA', DEFAULT_DB_SCHEMA_NAME)}.project.id"
user_needle_id = f"{os.environ.get('DB_SCHEMA', DEFAULT_DB_SCHEMA_NAME)}.user_needle.id"
user_yarn_id = f"{os.environ.get('DB_SCHEMA', DEFAULT_DB_SCHEMA_NAME)}.user_yarn.id"
user_gauge_id = f"{os.environ.get('DB_SCHEMA', DEFAULT_DB_SCHEMA_NAME)}.user_gauge.id"

project_needle = Table(
    "project_needle",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(project_id), primary_key=True),
    Column("needle_id", BigInteger, ForeignKey(user_needle_id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
    schema=os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME),
)

project_yarn = Table(
    "project_yarn",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(project_id), primary_key=True),
    Column("yarn_id", BigInteger, ForeignKey(user_yarn_id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
    Column("num_used", Float),
    schema=os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME),
)

project_gauge = Table(
    "project_gauge",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(project_id), primary_key=True),
    Column("gauge_id", BigInteger, ForeignKey(user_gauge_id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
    schema=os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME),
)
