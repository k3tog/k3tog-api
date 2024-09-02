from typing import List, Optional
from pydantic import BaseModel

from schemas.v1.photo import PhotoInfoV1


class UserYarnV1(BaseModel):
    id: int
    yarn_name: str
    brand_name: Optional[str]
    color: Optional[str]
    needle_range: Optional[tuple]
    hook_range: Optional[tuple]
    weight: Optional[float]
    note: Optional[str]
    created_ts: int
    updated_ts: int
    photos: Optional[List[PhotoInfoV1]]


class UserYarnCreateRequestInfoV1(BaseModel):
    yarn_name: str
    brand_name: Optional[str] = None
    color: Optional[str] = None
    needle_range_from: Optional[float] = None
    needle_range_to: Optional[float] = None
    hook_range_from: Optional[float] = None
    hook_range_to: Optional[float] = None
    weight: Optional[float] = None
    note: Optional[str] = None
    photo_ids: Optional[List[str]] = []
