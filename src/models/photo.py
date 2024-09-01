import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    String,
    func,
    Boolean,
)
from sqlalchemy.orm import relationship

from db.database import Base

logger = logging.getLogger(__name__)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    photo_id = Column(String(100), nullable=False)
    photo_key = Column(String(300), nullable=False)
    is_thumbnail = Column(Boolean, default=False)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    deleted_ts = Column(DateTime, nullable=True)
    type = Column(String(50), nullable=False)  # yarn, needle, project, gauge
    reference_id = Column(BigInteger, nullable=True)  # ID of the related entity

    user_yarn = relationship(
        "UserYarn",
        primaryjoin="and_(foreign(Photo.reference_id)==UserYarn.id, Photo.type=='user_yarn')",
        foreign_keys=[reference_id],
        back_populates="photos",
    )
    user_needle = relationship(
        "UserNeedle",
        primaryjoin="and_(foreign(Photo.reference_id)==UserNeedle.id, Photo.type=='user_needle')",
        foreign_keys=[reference_id],
        back_populates="photos",
    )
    user_gauge = relationship(
        "UserGauge",
        primaryjoin="and_(foreign(Photo.reference_id)==UserGauge.id, Photo.type=='user_gauge')",
        foreign_keys=[reference_id],
        back_populates="photos",
    )
    project = relationship(
        "Project",
        primaryjoin="and_(foreign(Photo.reference_id)==Project.id, Photo.type=='project')",
        foreign_keys=[reference_id],
        back_populates="photos",
    )

    def __repr__(self):
        return f"Photo(id={self.id!r}, photo_id={self.photo_id!r}, photo_key={self.photo_key!r}, is_thumbnail={self.is_thumbnail!r}, created_ts={self.created_ts!r}, deleted_ts={self.deleted_ts!r}, type={self.type!r}, reference_id={self.reference_id!r})"
