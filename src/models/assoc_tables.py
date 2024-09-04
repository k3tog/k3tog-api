import logging

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func, Float
from db.database import Base
from models.project import Project
from models.user_gauge import UserGauge
from models.user_needle import UserNeedle
from models.user_yarn import UserYarn


logger = logging.getLogger(__name__)

project_needle = Table(
    "project_needle",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(Project.id), primary_key=True),
    Column("needle_id", BigInteger, ForeignKey(UserNeedle.id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
)

project_yarn = Table(
    "project_yarn",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(Project.id), primary_key=True),
    Column("yarn_id", BigInteger, ForeignKey(UserYarn.id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
    Column("num_used", Float),
)

project_gauge = Table(
    "project_gauge",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey(Project.id), primary_key=True),
    Column("gauge_id", BigInteger, ForeignKey(UserGauge.id), primary_key=True),
    Column("created_ts", DateTime, server_default=func.now()),
    Column("updated_ts", DateTime, onupdate=func.now()),
)
