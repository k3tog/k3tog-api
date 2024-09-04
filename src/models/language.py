import logging
import os

from sqlalchemy import (
    BigInteger,
    Column,
    String,
)
from sqlalchemy.orm import Session
from db.database import DEFAULT_DB_SCHEMA_NAME, Base


logger = logging.getLogger(__name__)


class Language(Base):
    __tablename__ = "language"
    __table_args__ = {"schema": os.environ.get("DB_SCHEMA", DEFAULT_DB_SCHEMA_NAME)}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Language(id={self.id!r}, name={self.name!r})"

    @staticmethod
    def get_languages(session: Session):
        return session.query(Language).order_by(Language.name).all()

    @staticmethod
    def get_language_by_name(session: Session, name: str) -> "Language":
        return session.query(Language).filter_by(name=name).first()
