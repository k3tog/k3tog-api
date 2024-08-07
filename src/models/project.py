import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship, backref
from db.database import Base
from models.user import User
from models.user_pattern import UserPattern
from models.assoc_tables import project_needle, project_yarn


logger = logging.getLogger(__name__)


class Project(Base):
    __tablename__ = "project"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)
    co_date = Column(DateTime, nullable=True)
    fo_date = Column(DateTime, nullable=True)
    size = Column(String(50), nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    pattern_id = Column(BigInteger, ForeignKey(UserPattern.id), nullable=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # relationship with user_pattern table
    user_pattern = relationship(
        "UserPattern", backref=backref("projects", lazy="dynamic")
    )
    # many to many relationship to the user_needle table
    user_needles = relationship(
        "UserNeedle", secondary=project_needle, back_populates="projects"
    )
    # many to many relationship to the user_yarn table
    user_yarns = relationship(
        "UserYarn", secondary=project_yarn, back_populates="projects"
    )
