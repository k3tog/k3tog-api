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
from sqlalchemy.orm import relationship, Session
from db.database import Base
from models.user import User
from models.assoc_tables import project_needle


logger = logging.getLogger(__name__)


class UserNeedle(Base):
    __tablename__ = "user_needle"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    size = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # many-to-many relationship to the project table
    projects = relationship(
        "Project", secondary=project_needle, back_populates="user_needles"
    )

    photos = relationship(
        "Photo",
        primaryjoin="and_(foreign(Photo.reference_id)==UserNeedle.id, Photo.type=='user_needle')",
        back_populates="user_needle",
    )

    def __repr__(self):
        return f"UserNeedle(id={self.id!r}, name={self.name!r}, size={self.size!r}, note={self.note!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, user_id={self.user_id!r})"

    @staticmethod
    def get_user_needles_by_user_id(
        session: Session, user_id: int, exclude_deleted=True
    ):
        q = session.query(UserNeedle).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(UserNeedle.deleted_ts.is_(None))

        return q.all()

    @staticmethod
    def get_user_needle_by_needle_id_user_id(
        session: Session, needle_id: int, user_id: int
    ):
        return (
            session.query(UserNeedle)
            .filter_by(id=needle_id, user_id=user_id)
            .one_or_none()
        )
