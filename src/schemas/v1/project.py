from enum import Enum
from typing import List, Optional
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
    co_date: Optional[str] = None
    fo_date: Optional[str] = None
    pattern: Optional[UserPatternV1] = None
    size: Optional[str] = None
    yarns: Optional[List[UserYarnV1]] = []
    needles: Optional[List[UserNeedleV1]] = []
    note: Optional[str] = None


class ProjectCreateRequestInfoV1(BaseModel):
    title: str
    status: Optional[ProjectStatus] = ProjectStatus.NOT_STARTED
    co_date: Optional[str]  # "YYYY-MM-DD"
    fo_date: Optional[str]  # "YYYY-MM-DD"
    # TODO(irene): for patter, yarns, needles, if selected ones that already exist - just get pattern_id, yarn_id, needle_id.
    pattern: Optional[UserPatternCreateRequestInfoV1]
    size: Optional[str]
    yarns: Optional[List[UserYarnCreateRequestInfoV1]] = []
    needles: Optional[List[UserNeedleCreateRequestInfoV1]] = []
    note: Optional[str]
