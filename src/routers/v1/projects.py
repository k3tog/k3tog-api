import logging
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, status
from psycopg2.extras import NumericRange


from routers.utils import APITags
from schemas.v1.project import ProjectCreateRequestInfoV1, ProjectV1
from db.database import get_db_session
from models.user import User
from models.user_pattern import UserPattern
from models.user_yarn import UserYarn
from models.project import Project
from models.user_needle import UserNeedle
from services.project_manager import ProjectManager
from models.photo import Photo
from models.pattern_document import PatternDocument

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

        # if users selected existing pattern
        if type(project_create_req.pattern) == int:
            user_pattern = UserPattern.get_user_pattern_by_pattern_id_user_id(
                session=session, pattern_id=project_create_req.pattern, user_id=user.id
            )
        else:
            pattern_documents = []
            if project_create_req.pattern.pattern_document_id:
                pattern_document = PatternDocument.get_pattern_document_by_document_id(
                    session=session,
                    document_id=project_create_req.pattern.pattern_document_id,
                )
                pattern_documents = [pattern_document]

            user_pattern = UserPattern(
                name=project_create_req.pattern.name,
                author=project_create_req.pattern.author,
                description=project_create_req.pattern.description,
                user_id=user.id,
                pattern_documents=pattern_documents,
            )
            session.add(user_pattern)

        user_yarns = []
        for yarn in project_create_req.yarns:
            if type(yarn) == int:
                user_yarn = UserYarn.get_user_yarn_by_yarn_id_user_id(
                    session=session, yarn_id=yarn, user_id=user.id
                )
            else:
                photos = Photo.get_photos_by_photo_ids(
                    session=session, photo_ids=yarn.photo_ids
                )
                user_yarn = UserYarn(
                    yarn_name=yarn.yarn_name,
                    brand_name=yarn.brand_name,
                    color=yarn.color,
                    needle_range=NumericRange(
                        yarn.needle_range_from,
                        yarn.needle_range_to,
                    ),
                    hook_range=NumericRange(yarn.hook_range_from, yarn.hook_range_to),
                    weight=yarn.weight,
                    note=yarn.note,
                    user_id=user.id,
                )
                session.add(user_yarn)
                session.flush()

                for photo in photos:
                    photo.reference_id = user_yarn.id
                    photo.type = "user_yarn"

            user_yarns.append(user_yarn)

        user_needles = []
        for needle in project_create_req.needles:
            if type(needle) == int:
                user_needle = UserNeedle.get_user_needle_by_needle_id_user_id(
                    session=session, needle_id=needle, user_id=user.id
                )
            else:
                photos = Photo.get_photos_by_photo_ids(
                    session=session, photo_ids=needle.photo_ids
                )
                user_needle = UserNeedle(
                    name=needle.name,
                    size=needle.size,
                    note=needle.note,
                    user_id=user.id,
                )
                session.add(user_needle)
                session.flush()

                for photo in photos:
                    photo.reference_id = user_needle.id
                    photo.type = "user_needle"

            user_needles.append(user_needle)

        # TODO(irene): add gauges

        project = Project(
            title=project_create_req.title,
            status=project_create_req.status,
            co_date=(
                datetime.strptime(project_create_req.co_date, "%Y-%m-%d")
                if project_create_req.co_date
                else None
            ),
            fo_date=(
                datetime.strptime(project_create_req.fo_date, "%Y-%m-%d")
                if project_create_req.fo_date
                else None
            ),
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
