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
from sqlalchemy.orm import relationship, backref, Session
from db.database import Base
from models.user import User
from models.user_pattern import UserPattern
from models.assoc_tables import project_needle, project_yarn, project_gauge


logger = logging.getLogger(__name__)


class Project(Base):
    __tablename__ = "project"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)
    co_date = Column(DateTime, nullable=True)
    fo_date = Column(DateTime, nullable=True)
    size = Column(String(50), nullable=True)
    note = Column(Text, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    pattern_id = Column(BigInteger, ForeignKey(UserPattern.id), nullable=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # relationship with user_pattern table
    user_pattern = relationship(
        "UserPattern", backref=backref("projects", lazy="dynamic")
    )
    # many to many relationship to the user_needle table
    user_needles = relationship(
        "UserNeedle", secondary=project_needle, back_populates="projects"
    )
    # many to many relationship to the user_yarn table
    user_yarns = relationship(
        "UserYarn", secondary=project_yarn, back_populates="projects"
    )
    # many to many relationship to the user_gauge table
    user_gauges = relationship(
        "UserGauge", secondary=project_gauge, back_populates="projects"
    )

    def __repr__(self):
        return f"Project(id={self.id!r}, title={self.title!r}, status={self.status!r}, co_date={self.co_date!r}, fo_date={self.fo_date!r}, size={self.size!r}, note={self.note!r}, created_ts={self.created_ts!r}, updated_ts={self.updated_ts!r}, deleted_ts={self.deleted_ts!r}, pattern_id={self.pattern_id!r}, user_id={self.user_id!r})"

    @staticmethod
    def get_projects_by_user_id(session: Session, user_id: int, exclude_deleted=True):
        q = session.query(Project).filter_by(user_id=user_id)
        if exclude_deleted:
            q = q.filter(Project.deleted_ts.is_(None))

        return q.all()

    @staticmethod
    def get_project_by_project_id_user_id(
        session: Session, project_id: int, user_id: int
    ):
        return (
            session.query(Project)
            .filter_by(id=project_id, user_id=user_id)
            .one_or_none()
        )
