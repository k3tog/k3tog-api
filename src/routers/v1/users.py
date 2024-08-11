import logging

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status

from routers.utils import APITags
from schemas.v1.user import UserCreateRequestInfoV1, UserV1
from db.database import get_db_session
from models.user import User
from services.user_manager import UserManager

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
        # fetch all existing users
        users = User.get_users(session=session)

        # convert the db models to pydantic schema
        user_infos = []
        user_manager = UserManager()
        for user in users:
            user_infos.append(user_manager.convert_user_to_user_v1(user))


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
    with get_db_session() as session:
        # check if there's an user with the same email or same username
        user_by_username = User.get_user_by_username(
            session=session,
            username=user_create_req.username,
        )
        user_by_email = User.get_user_by_email(
            session=session, email=user_create_req.email
        )

        if user_by_username or user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with the requested email or username already exists!",
            )


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
