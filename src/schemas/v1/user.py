from typing import Optional

from pydantic import BaseModel, PositiveInt


class UserV1(BaseModel):
    id: int
    external_id: Optional[str] = None
    username: str
    email: str
    location: Optional[str] = None
    birthday: Optional[str] = None
    knitting_since: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    preferred_language: Optional[str]
    created_ts: int
    updated_ts: int
    deactivated_ts: Optional[int] = None


class UserCreateRequestInfoV1(BaseModel):
    username: str
    email: str
    state: Optional[str]
    country: Optional[str]
    birthday_year: Optional[PositiveInt]
    birthday_month: Optional[PositiveInt]
    birthday_day: Optional[PositiveInt]
    knitting_since: Optional[PositiveInt]
    bio: Optional[str]
    avatar_url: Optional[str]  # TODO(irene): set the default url
    preferred_language: Optional[str] = "English"
