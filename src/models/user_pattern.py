import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    func,
)
from db.database import Base
from sqlalchemy.orm import Session
from models.user import User


logger = logging.getLogger(__name__)


class UserPattern(Base):
    __tablename__ = "user_pattern"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    author = Column(String(100), nullable=True)
    file_attachment = Column(String(500), nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f"UserPattern(id={self.id!r}, name={self.name!r}, author={self.author!r}, file_attachment={self.file_attachment!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, user_id={self.user_id!r})"

    @staticmethod
    def get_user_patterns_by_user_id(
        session: Session, user_id: int, exclude_deleted=True
    ):
        q = session.query(UserPattern).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(UserPattern.deleted_ts.is_(None))

        return q.all()
