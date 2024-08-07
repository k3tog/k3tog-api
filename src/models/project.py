import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship, backref
from db.database import Base
from models.user import User
from models.user_pattern import UserPattern


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
