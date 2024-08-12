import logging

from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status

from routers.utils import APITags
from schemas.v1.user import UserCreateRequestInfoV1, UserV1
from db.database import get_db_session
from models.user import User
from services.user_manager import UserManager
from models.language import Language

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
            user_infos.append(user_manager.convert_user_to_user_v1(user=user))

    return user_infos


# `GET /v1/users/{username}`
@router.get(
    "/users/{username}",
    tags=[APITags.users],
    description="Get a single user using username",
    response_model=UserV1,
    response_model_exclude_none=True,
)
async def get_user(username: Annotated[str, Path(title="Username of the user to get")]):
    with get_db_session() as session:
        # fetch the specified user by username
        user = User.get_user_by_username(session=session, username=username)

        if user:
            return UserManager().convert_user_to_user_v1(user=user)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")


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

        # TODO(irene): more verification logics

        birthday_dt = datetime(
            user_create_req.birthday_year,
            user_create_req.birthday_month,
            user_create_req.birthday_day,
        )

        # NOTE(irene): temporarily set English as preferred language by default
        language = Language.get_language_by_name(
            session=session, name=user_create_req.preferred_language
        )

        user = User(
            username=user_create_req.username,
            email=user_create_req.email,
            location_state=user_create_req.state,
            location_country=user_create_req.country,
            birthday=birthday_dt,
            knitting_since=user_create_req.knitting_since,
            bio=user_create_req.bio,
            avatar_url=user_create_req.avatar_url,
            preferred_language_id=language.id,
        )

        session.add(user)
        session.commit()

        return UserManager().convert_user_to_user_v1(user=user)


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
