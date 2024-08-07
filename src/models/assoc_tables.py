import logging

from sqlalchemy import BigInteger, Column, ForeignKey, Table
from db.database import Base


logger = logging.getLogger(__name__)

project_needle = Table(
    "project_needle",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("project.id"), primary_key=True),
    Column("needle_id", BigInteger, ForeignKey("user_needle.id"), primary_key=True),
)

project_yarn = Table(
    "project_yarn",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("project.id"), primary_key=True),
    Column("needle_id", BigInteger, ForeignKey("user_yarn.id"), primary_key=True),
)
