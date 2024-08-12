import logging
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, status

from routers.utils import APITags
from schemas.v1.project import ProjectCreateRequestInfoV1, ProjectV1
from db.database import get_db_session
from models.user import User
from models.user_pattern import UserPattern
from models.user_yarn import UserYarn
from models.project import Project
from models.user_needle import UserNeedle
from services.project_manager import ProjectManager

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/{username}/projects/`
@router.get(
    "/v1/users/{username}/projects/",
    tags=[APITags.projects],
    description="Get a list of projects for the user",
    response_model=List[ProjectV1],
    response_model_exclude_none=True,
)
async def get_projects(
    username: Annotated[
        str, Path(title="Username of the user to get a list of projects for")
    ]
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        # fetch all projects that the user owns
        projects = Project.get_projects_by_user_id(session=session, user_id=user.id)

    project_info = []
    project_manager = ProjectManager()
    for project in projects:
        project_info.append(
            project_manager.convert_project_to_project_v1(project=project)
        )

    return project_info


# `GET /v1/users/{username}/projects/{project_id}/`
@router.get(
    "/v1/users/{username}/projects/{project_id}",
    tags=[APITags.projects],
    description="Get a single project for the user",
    response_model=ProjectV1,
    response_model_exclude_none=True,
)
async def get_project(
    username: Annotated[
        str, Path(title="Username of the user to get a list of projects for")
    ],
    project_id: Annotated[int, Path(title="ID of the project")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        project = Project.get_project_by_project_id_user_id(
            session=session, project_id=project_id, user_id=user.id
        )

    if project:
        return ProjectManager().convert_project_to_project_v1(project=project)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No project found"
    )


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
    project_create_req: ProjectCreateRequestInfoV1,
    username: Annotated[str, Path(title="Username of the user to get user's projects")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_pattern = UserPattern(
            name=project_create_req.pattern.name,
            author=project_create_req.pattern.author,
            user_id=user.id,
        )
        session.add(user_pattern)

        user_yarns = []
        for yarn in project_create_req.yarns:
            user_yarn = UserYarn(
                name=yarn.name,
                color=yarn.color,
                note=yarn.note,
                num_used=yarn.num_used,
                user_id=user.id,
            )
            session.add(user_yarn)
            user_yarns.append(user_yarn)

        user_needles = []
        for needle in project_create_req.needles:
            user_needle = UserNeedle(
                name=needle.name,
                size=needle.size,
                note=needle.note,
                user_id=user.id,
            )
            session.add(user_needle)
            user_needles.append(user_needle)

        project = Project(
            title=project_create_req.title,
            status=project_create_req.status,
            co_date=datetime.strptime(project_create_req.co_date, "%Y-%m-%d"),
            fo_date=datetime.strptime(project_create_req.fo_date, "%Y-%m-%d"),
            size=project_create_req.size,
            note=project_create_req.note,
            user_pattern=user_pattern,
            user_yarns=user_yarns,
            user_needles=user_needles,
            user_id=user.id,
        )
        session.add(project)
        session.commit()

        return ProjectManager().convert_project_to_project_v1(project=project)


# `PUT /v1/users/{username}/projects/{project_id}`

# `DELETE /v1/users/{username}/projects/{project_id}`
