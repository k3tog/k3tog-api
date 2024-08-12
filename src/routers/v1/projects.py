import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from routers.utils import APITags
from schemas.v1.project import ProjectCreateRequestInfoV1, ProjectV1

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/{username}/projects/`

# `GET /v1/users/{username}/projects/{project_id}/`


# `POST /v1/users/{username}/projects/`
@router.post(
    "/v1/users/{username}/projects/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.projects],
    description="Create a new project for the user",
    response_model=ProjectV1,
    response_model_exclude_none=True,
)
async def create_project(
    project_create_rea: ProjectCreateRequestInfoV1,
    username: Annotated[str, Path(title="Username of the user to get user's projects")],
):
    pass


# `PUT /v1/users/{username}/projects/{project_id}`

# `DELETE /v1/users/{username}/projects/{project_id}`
