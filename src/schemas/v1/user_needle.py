from typing import List, Optional
from pydantic import BaseModel

from schemas.v1.photo import PhotoInfoV1


class UserNeedleV1(BaseModel):
    id: int
    name: str
    size: Optional[str]
    note: Optional[str]
    created_ts: int
    updated_ts: int
    photos: Optional[List[PhotoInfoV1]] = []


class UserNeedleCreateRequestInfoV1(BaseModel):
    name: str
    size: Optional[str] = None
    note: Optional[str] = None
    photo_ids: Optional[List[str]] = []
