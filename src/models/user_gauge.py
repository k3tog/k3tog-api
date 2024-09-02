import logging

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from db.database import Base
from models.assoc_tables import project_gauge
from models.user import User
from models.user_needle import UserNeedle
from models.user_yarn import UserYarn

logger = logging.getLogger(__name__)


class UserGauge(Base):
    __tablename__ = "user_gauge"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stitches = Column(Float, nullable=True)
    rows = Column(Float, nullable=True)
    after_wash = Column(Boolean, nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    needle_id = Column(BigInteger, ForeignKey(UserNeedle.id), nullable=True)
    yarn_id = Column(BigInteger, ForeignKey(UserYarn.id), nullable=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # many-to-many relationship to the project table
    projects = relationship(
        "Project", secondary=project_gauge, back_populates="user_gauges"
    )

    def __repr__(self):
        return f"UesrGauge(id={self.id!r}, stitches={self.stitches!r}, rows={self.rows!r}, after_wash={self.after_wash!r}, note={self.note!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, needle_id={self.needle_id!r}, yarn_id={self.yarn_id!r})"
