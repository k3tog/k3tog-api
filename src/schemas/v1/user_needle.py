from typing import Optional
from pydantic import BaseModel


class UserNeedleV1(BaseModel):
    id: int
    name: str
    size: Optional[str]
    note: Optional[str]
    created_ts: int
    updated_ts: int


class UserNeedleCreateRequestInfoV1(BaseModel):
    name: str
    size: Optional[str]
    note: Optional[str]
