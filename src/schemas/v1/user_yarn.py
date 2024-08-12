from typing import Optional
from pydantic import BaseModel


class UserYarnV1(BaseModel):
    id: int
    name: str
    color: Optional[str]
    note: Optional[str]
    num_used: Optional[float]
    created_ts: int
    updated_ts: int


class UserYarnCreateRequestInfoV1(BaseModel):
    name: str
    color: Optional[str]
    note: Optional[str]
    num_used: Optional[float]
