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
from models.user_pattern import UserPattern


logger = logging.getLogger(__name__)


class PatternDocument(Base):
    __tablename__ = "pattern_document"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_reference = Column(String(100), nullable=False)
    filename_display = Column(String(150))
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    pattern_id = Column(BigInteger, ForeignKey(UserPattern.id), nullable=False)

    def __repr__(self):
        return f"PatternDocument(id={self.id!r}, file_reference={self.file_reference!r}, filename_display={self.filename_display!r}, created_ts={self.created_ts!r}, deleted_ts={self.deleted_ts}, pattern_id={self.pattern_id!r})"
