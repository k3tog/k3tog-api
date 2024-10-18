from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from schemas.v1.user_pattern import UserPatternCreateRequestInfoV1, UserPatternV1
from schemas.v1.user_yarn import UserYarnCreateRequestInfoV1, UserYarnV1
from schemas.v1.user_needle import UserNeedleCreateRequestInfoV1, UserNeedleV1
from schemas.v1.user_gauge import UserGaugeCreateRequestInfoV1
from schemas.v1.photo import PhotoInfoV1


class ProjectStatus(str, Enum):
    NOT_STARTED = "Not Started"
    WIP = "Work in Progress"
    FINISHED = "Finished"


class ProjectV1(BaseModel):
    id: int
    title: str
    status: Optional[ProjectStatus] = ProjectStatus.NOT_STARTED
    co_date: Optional[str] = None
    fo_date: Optional[str] = None
    pattern: Optional[UserPatternV1] = None
    size: Optional[str] = None
    yarns: Optional[List[UserYarnV1]] = []
    needles: Optional[List[UserNeedleV1]] = []
    note: Optional[str] = None
    photos: Optional[List[PhotoInfoV1]] = []


class ProjectCreateRequestInfoV1(BaseModel):
    title: str
    status: Optional[ProjectStatus] = ProjectStatus.NOT_STARTED
    co_date: Optional[str] = None  # "YYYY-MM-DD"
    fo_date: Optional[str] = None  # "YYYY-MM-DD"
    size: Optional[str] = None
    pattern: Optional[Union[UserPatternCreateRequestInfoV1, int]] = None
    yarns: Optional[List[Union[UserYarnCreateRequestInfoV1, int]]] = []
    needles: Optional[List[Union[UserNeedleCreateRequestInfoV1, int]]] = []
    gauges: Optional[List[Union[UserGaugeCreateRequestInfoV1, int]]] = []
    note: Optional[str] = None
    photo_ids: Optional[List[str]] = []
