import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    func, 
    Text
)
from db.database import Base
from sqlalchemy.orm import Session, relationship
from models.user import User


logger = logging.getLogger(__name__)


class UserPattern(Base):
    __tablename__ = "user_pattern"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    author = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # relationship to the project table
    pattern_documents = relationship("PatternDocument", backref="user_pattern", cascade="all, delete-orphan")

    def __repr__(self):
        return f"UserPattern(id={self.id!r}, name={self.name!r}, author={self.author!r}, description={self.description!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, user_id={self.user_id!r})"

    @staticmethod
    def get_user_patterns_by_user_id(
        session: Session, user_id: int, exclude_deleted=True
    ):
        q = session.query(UserPattern).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(UserPattern.deleted_ts.is_(None))

        return q.all()

    @staticmethod
    def get_user_pattern_by_pattern_id_user_id(
        session: Session, pattern_id: int, user_id: int
    ):
        return (
            session.query(UserPattern)
            .filter_by(id=pattern_id, user_id=user_id)
            .one_or_none()
        )
