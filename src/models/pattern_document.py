import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Session
from db.database import Base


logger = logging.getLogger(__name__)


class PatternDocument(Base):
    __tablename__ = "pattern_document"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_id = Column(String(100), nullable=False)
    document_key = Column(String(250), nullable=False)
    filename_display = Column(String(150))
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    deleted_ts = Column(DateTime, nullable=True)

    pattern_id = Column(
        BigInteger, ForeignKey("user_pattern.id"), nullable=True
    )  # Allow NULL pattern_id

    def __repr__(self):
        return f"PatternDocument(id={self.id!r}, document_id={self.document_id!r}, document_key={self.document_key!r}, filename_display={self.filename_display!r}, created_ts={self.created_ts!r}, deleted_ts={self.deleted_ts}, pattern_id={self.pattern_id!r})"

    @staticmethod
    def get_pattern_document_by_document_id(session: Session, document_id: str):
        return (
            session.query(PatternDocument)
            .filter_by(document_id=document_id)
            .one_or_none()
        )
