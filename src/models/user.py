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
from sqlalchemy.orm import relationship, backref, Session
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
    # relationship to the user_gauge table
    user_gauges = relationship(
        "UserGauge", backref="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, external_id={self.external_id!r}, username={self.username!r}, email={self.email!r}, location_state={self.location_state!r}, location_country={self.location_country!r}, birthday={self.birthday!r}, knitting_since={self.knitting_since!r}, bio={self.bio!r}, avatar_url={self.avatar_url!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deactivated_ts={self.deactivated_ts!r}, preferred_language_id={self.preferred_language_id!r})"

    @staticmethod
    def get_users(session: Session):
        return session.query(User).order_by(User.username).all()

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> "User":
        return (
            session.query(User)
            .filter_by(username=username.lower())
            .order_by(User.username)
            .first()
        )

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> "User":
        return (
            session.query(User)
            .filter_by(email=email.lower())
            .order_by(User.username)
            .first()
        )
