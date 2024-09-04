from datetime import datetime
import logging
import os

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Text,
    func,
    String,
)
from sqlalchemy.orm import relationship, Session
from db.database import DEFAULT_DB_SCHEMA_NAME, Base
from models.assoc_tables import project_gauge
from models.user import User
from models.user_yarn import UserYarn

logger = logging.getLogger(__name__)


class UserGauge(Base):
    __tablename__ = "user_gauge"
    __table_args__ = {"schema": os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME)}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    yarn_description = Column(String(500), nullable=True)
    needle_size = Column(String(100), nullable=True)
    stitches = Column(Float, nullable=True)
    rows = Column(Float, nullable=True)
    # after_wash = Column(Boolean, nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    yarn_id = Column(BigInteger, ForeignKey(UserYarn.id), nullable=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # many-to-many relationship to the project table
    projects = relationship(
        "Project", secondary=project_gauge, back_populates="user_gauges"
    )

    def __repr__(self):
        return f"UesrGauge(id={self.id!r}, stitches={self.stitches!r}, rows={self.rows!r}, after_wash={self.after_wash!r}, note={self.note!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, needle_id={self.needle_id!r}, yarn_id={self.yarn_id!r})"

    @staticmethod
    def get_user_gauges_by_user_id(
        session: Session, user_id: int, exclude_deleted=True
    ):
        q = session.query(UserGauge).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(UserGauge.deleted_ts.is_(None))

        return q.all()

    @staticmethod
    def get_user_gauge_by_gauge_id_user_id(
        session: Session, gauge_id: int, user_id: int
    ):
        return (
            session.query(UserGauge)
            .filter_by(id=gauge_id, user_id=user_id)
            .one_or_none()
        )

    @staticmethod
    def delete_user_gauge_by_gauge_id_user_id(
        session: Session, gauge_id: int, user_id: int
    ):
        user_gauge = UserGauge.get_user_gauge_by_gauge_id_user_id(
            session=session, gauge_id=gauge_id, user_id=user_id
        )
        if not user_gauge:
            return None

        user_gauge.deleted_ts = datetime.now()
        return user_gauge
