import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from db.database import Base
from models.user import User
from models.assoc_tables import project_yarn

logger = logging.getLogger(__name__)


class UserYarn(Base):
    __tablename__ = "user_yarn"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    color = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)
    num_used = Column(Float, nullable=True)
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)

    # many-to-many relationship to the project table
    projects = relationship(
        "Project", secondary=project_yarn, back_populates="user_yarns"
    )


#     My Yarn
# yarn_id	integer	PK
# name	varchar
# color	varchar
# note	varchar
# num_used	float
# created_ts	datetime
# updated_ts	datetime
# deleted_ts	datetime
# user_id	integer	FK
