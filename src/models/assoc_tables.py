import logging
import os

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func, Float
from db.database import DEFAULT_DB_SCHEMA_NAME, Base


logger = logging.getLogger(__name__)

project_needle = Table(
    "project_needle",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("project.id"), primary_key=True),
    Column("needle_id", BigInteger, ForeignKey("user_needle.id"), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
)

project_yarn = Table(
    "project_yarn",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("project.id"), primary_key=True),
    Column("yarn_id", BigInteger, ForeignKey("user_yarn.id"), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
    Column("num_used", Float),
)

project_gauge = Table(
    "project_gauge",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("project.id"), primary_key=True),
    Column("gauge_id", BigInteger, ForeignKey("user_gauge.id"), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
)
