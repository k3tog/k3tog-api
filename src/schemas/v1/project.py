from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from schemas.v1.user_pattern import UserPatternCreateRequestInfoV1, UserPatternV1
from schemas.v1.user_yarn import UserYarnCreateRequestInfoV1, UserYarnV1
from schemas.v1.user_needle import UserNeedleCreateRequestInfoV1, UserNeedleV1


class ProjectStatus(str, Enum):
    NOT_STARTED = "Not Started"
    WIP = "Work in Progress"
    FINISHED = "Finished"


class ProjectV1(BaseModel):
    id: int
    title: str
    status: Optional[ProjectStatus] = ProjectStatus.NOT_STARTED
    co_date: Optional[str]
    fo_date: Optional[str]
    pattern: Optional[UserPatternV1]
    size: Optional[str]
    yarn: Optional[UserYarnV1]
    needle: Optional[UserNeedleV1]
    note: Optional[str]


class ProjectCreateRequestInfoV1(BaseModel):
    title: str
    status: Optional[ProjectStatus] = ProjectStatus.NOT_STARTED
    co_date: Optional[datetime]
    fo_date: Optional[datetime]
    pattern: Optional[UserPatternCreateRequestInfoV1]
    size: Optional[str]
    yarn: Optional[UserYarnCreateRequestInfoV1]
    needle: Optional[UserNeedleCreateRequestInfoV1]
    note: Optional[str]
