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
from models.language import Language


logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    external_id = Column(String(50), nullable=True, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    location_state = Column(String(50), nullable=True)
    location_country = Column(String(50), nullable=True)
    birthday = Column(DateTime, nullable=True)
    knitting_since = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deactivated_ts = Column(DateTime, nullable=True)

    preferred_language_id = Column(BigInteger, ForeignKey(Language.id), nullable=False)

    # relationship to the language table
    preferred_language = relationship(
        "Language", backref=backref("users", lazy="dynamic")
    )
    # relationship to the project table
    projects = relationship("Project", backref="user", cascade="all, delete-orphan")
    # relationship to the user_pattern table
    user_patterns = relationship(
        "UserPattern", backref="user", cascade="all, delete-orphan"
    )
    # relationship to the user_needle table
    user_needles = relationship(
        "UserNeedle", backref="user", cascade="all, delete-orphan"
    )
    # relationship to the user_yarn table
    user_yarns = relationship("UserYarn", backref="user", cascade="all, delete-orphan")
