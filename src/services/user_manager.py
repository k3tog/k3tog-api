import logging

from schemas.v1.user import UserV1

logger = logging.getLogger()


class UserManager:
    def convert_user_to_user_v1(self, user):
        return UserV1(
            id=user.id,
            external_id=user.external_id,
            username=user.username,
            email=user.email,
        )


# class UserV1(BaseModel):
#     id: int
#     external_id: str
#     username: str
#     email: str
#     location: Optional[str] = None
#     birthday: Optional[str] = None
#     knitting_since: Optional[str] = None
#     bio: Optional[str] = None
#     avatar_url: Optional[str] = None
#     created_ts: int
#     updated_ts: int
#     deactivated_ts: Optional[int] = None

# id = Column(BigInteger, primary_key=True, autoincrement=True)
#     external_id = Column(String(50), nullable=True, unique=True)
#     username = Column(String(50), nullable=False, unique=True)
#     email = Column(String(100), nullable=False, unique=True)
#     location_state = Column(String(50), nullable=True)
#     location_country = Column(String(50), nullable=True)
#     birthday = Column(DateTime, nullable=True)
#     knitting_since = Column(Integer, nullable=True)
#     bio = Column(Text, nullable=True)
#     avatar_url = Column(String(500), nullable=True)
#     created_ts = Column(DateTime, nullable=False, server_default=func.now())
#     updated_ts = Column(DateTime, nullable=True, onupdate=func.now())
#     deactivated_ts = Column(DateTime, nullable=True)

#     preferred_language_id = Column(BigInteger, ForeignKey(Language.id), nullable=False)
