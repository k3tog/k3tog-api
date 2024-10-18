from typing import Optional
from pydantic import BaseModel


class PhotoInfoV1(BaseModel):
    id: int
    photo_id: str
    photo_key: str
    signed_photo_url: Optional[str]
    is_thumbnail: bool
    created_ts: int
    type: str  # TODO(irene): change to enum
