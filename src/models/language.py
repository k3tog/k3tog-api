import logging

from sqlalchemy import (
    BigInteger,
    Column,
    String,
)
from db.database import Base


logger = logging.getLogger(__name__)


class Language(Base):
    __tablename__ = "language"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Language(id={self.id!r}, name={self.name!r})"
