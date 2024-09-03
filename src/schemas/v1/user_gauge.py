from typing import Optional
from pydantic import BaseModel

from schemas.v1.photo import PhotoInfoV1
from schemas.v1.user_yarn import UserYarnV1


class UserGaugeV1(BaseModel):
    id: int
    yarn_description: Optional[str]
    yarn: Optional[UserYarnV1] = None
    needle_size: Optional[str]
    stitches: Optional[float]
    rows: Optional[float]
    note: Optional[str]
    created_ts: int
    updated_ts: int
    photo: Optional[PhotoInfoV1]


class UserGaugeCreateRequestInfoV1(BaseModel):
    yarn_description: Optional[str]
    yarn_id: Optional[int] = None
    needle_size: Optional[str]
    stitches: Optional[float]
    rows: Optional[float]
    note: Optional[str]
    photo_id: Optional[str] = None
