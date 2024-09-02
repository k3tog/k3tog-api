import logging
from typing import List

from sqlalchemy import BigInteger, Column, DateTime, String, func, Boolean, Integer
from sqlalchemy.orm import relationship, Session

from db.database import Base
from models.project import Project
from models.user_gauge import UserGauge
from models.user_needle import UserNeedle
from models.user_yarn import UserYarn

logger = logging.getLogger(__name__)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    photo_id = Column(String(100), nullable=False)
    photo_key = Column(String(300), nullable=False)
    is_thumbnail = Column(Boolean, default=False)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    deleted_ts = Column(DateTime, nullable=True)
    type = Column(String(50), nullable=True)  # user_yarn, user_needle, project, gauge
    reference_id = Column(Integer, nullable=True)  # ID of the related entity

    @property
    def entity(self, session: Session):
        if self.type == "project":
            return session.query(Project).get(self.reference_id)
        elif self.type == "user_yarn":
            return session.query(UserYarn).get(self.reference_id)
        elif self.type == "user_needle":
            return session.query(UserNeedle).get(self.reference_id)
        elif self.type == "user_gauge":
            return session.query(UserGauge).get(self.reference_id)
        else:
            return None

    def __repr__(self):
        return f"Photo(id={self.id!r}, photo_id={self.photo_id!r}, photo_key={self.photo_key!r}, is_thumbnail={self.is_thumbnail!r}, created_ts={self.created_ts!r}, deleted_ts={self.deleted_ts!r}, type={self.type!r}, reference_id={self.reference_id!r})"

    @staticmethod
    def get_photos_by_photo_ids(session: Session, photo_ids: List[str]):
        return session.query(Photo).filter(Photo.photo_id.in_(photo_ids)).all()

    @staticmethod
    def get_photos_by_reference_id_type(session: Session, reference_id: int, type: str):
        return (
            session.query(Photo)
            .filter(Photo.reference_id == reference_id, Photo.type == type)
            .all()
        )
