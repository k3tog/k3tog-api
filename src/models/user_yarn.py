import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    Numeric,
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import NUMRANGE

from db.database import Base
from models.user import User
from models.assoc_tables import project_yarn

logger = logging.getLogger(__name__)


class UserYarn(Base):
    __tablename__ = "user_yarn"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    yarn_name = Column(String(300), nullable=False)
    brand_name = Column(String(300), nullable=True)
    color = Column(String(100), nullable=True)
    needle_range = Column(NUMRANGE, nullable=True)
    hook_range = Column(NUMRANGE, nullable=True)
    weight = Column(Numeric(7, 2), nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # many-to-many relationship to the project table
    projects = relationship(
        "Project", secondary=project_yarn, back_populates="user_yarns"
    )

    def __repr__(self):
        return f"UserYarn(id={self.id!r}, yarn_name={self.yarn_name!r}, brand_name={self.brand_name}, color={self.color!r}, needle_range={self.needle_range!r}, hook_range={self.hook_range!r}, weight={self.weight!r}, note={self.note!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, user_id={self.user_id!r})"

    @staticmethod
    def get_user_yarns_by_user_id(session: Session, user_id: int, exclude_deleted=True):
        q = session.query(UserYarn).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(UserYarn.deleted_ts.is_(None))

        return q.all()

    @staticmethod
    def get_user_yarn_by_yarn_id_user_id(session: Session, yarn_id: int, user_id: int):
        return (
            session.query(UserYarn).filter_by(id=yarn_id, user_id=user_id).one_or_none()
        )
