import logging

from typing import Annotated, List
from fastapi import APIRouter, Path, status

from routers.utils import APITags
from schemas.v1.user import UserCreateRequestInfoV1, UserV1
from db.database import get_db_session

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/`
@router.get(
    "/users/",
    tags=[APITags.users],
    description="Get a list of users",
    response_model=List[UserV1],
    response_model_exclude_none=True,
)
async def get_users():
    with get_db_session() as session:
        # fetch all users
        pass


# `GET /v1/users/{user_id}`
@router.get(
    "/users/{user_id}",
    tags=[APITags.users],
    description="Get a single user using user_id",
    response_model=UserV1,
    response_model_exclude_none=True,
)
async def get_user(user_id: Annotated[int, Path(title="ID of the user to get")]):
    pass


# `POST /v1/users/`
@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.users],
    description="Create a single user",
    response_model=UserV1,
    response_model_exclude_none=True,
)
async def create_user(user_create_req: UserCreateRequestInfoV1):
    pass


# `PUT /v1/users/{user_id}`
@router.put(
    "/users/{user_id}",
    tags=[APITags.users],
    description="Update a single user",
    response_model=UserV1,
    response_model_exclude_none=True,
)
async def update_user():
    pass
