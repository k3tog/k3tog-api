from typing import Optional
from pydantic import BaseModel


class UserPatternV1(BaseModel):
    id: int
    name: str
    author: Optional[str]
    created_ts: int
    updated_ts: int


class UserPatternCreateRequestInfoV1(BaseModel):
    name: str
    author: Optional[str]
    # TODO(irene): reference for file attachment?
