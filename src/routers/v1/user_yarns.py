import logging

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status
from psycopg2.extras import NumericRange
from routers.utils import APITags
from db.database import get_db_session
from models.user import User
from schemas.v1.user_yarn import UserYarnCreateRequestInfoV1, UserYarnV1
from models.user_yarn import UserYarn
from services.user_yarn_manager import UserYarnManager

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/{username}/yarns/`
@router.get(
    "/v1/users/{username}/yarns/",
    tags=[APITags.yarns],
    description="Get a list of yarns for the user",
    response_model=List[UserYarnV1],
    response_model_exclude_none=True,
)
async def get_user_yarns(
    username: Annotated[
        str, Path(title="Username of the user to get a list of patterns for")
    ]
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_yarns = UserYarn.get_user_yarns_by_user_id(
            session=session, user_id=user.id
        )

    user_yarn_info = []
    user_yarn_manager = UserYarnManager()
    for user_yarn in user_yarns:
        user_yarn_info.append(
            user_yarn_manager.convert_user_yarn_to_user_yarn_v1(user_yarn=user_yarn)
        )

    return user_yarn_info


# `GET /v1/users/{username}/yarns/{yarn_id}/`
@router.get(
    "/v1/users/{username}/yarns/{yarn_id}",
    tags=[APITags.yarns],
    description="Get a single yarn for the user",
    response_model=UserYarnV1,
    response_model_exclude_none=True,
)
async def get_user_yarn(
    username: Annotated[
        str, Path(title="Username of the user to get a list of yarns for")
    ],
    yarn_id: Annotated[int, Path(title="ID of the yarn")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_yarn = UserYarn.get_user_yarn_by_yarn_id_user_id(
            session=session, yarn_id=yarn_id, user_id=user.id
        )

    if user_yarn:
        return UserYarnManager().convert_user_yarn_to_user_yarn_v1(user_yarn=user_yarn)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No yarn found")


# `POST /v1/users/{username}/yarns/`
@router.post(
    "/v1/users/{username}/yarns/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.yarns],
    description="Create a new yarn for the user",
    response_model=UserYarnV1,
    response_model_exclude_none=True,
)
async def create_user_yarn(
    yarn_create_req: UserYarnCreateRequestInfoV1,
    username: Annotated[
        str, Path(title="Username of the user to create a new yarn for")
    ],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )
        
        # TODO(irene): implement api endpoint for uploading multiple photos and connect them to here

        user_yarn = UserYarn(
            yarn_name=yarn_create_req.yarn_name,
            brand_name=yarn_create_req.brand_name,
            color=yarn_create_req.color,
            needle_range=NumericRange(
                yarn_create_req.needle_range_from, yarn_create_req.needle_range_to
            ),
            hook_range=NumericRange(
                yarn_create_req.hook_range_from, yarn_create_req.hook_range_to
            ),
            weight=yarn_create_req.weight,
            note=yarn_create_req.note,
            user_id=user.id,
        )

        session.add(user_yarn)
        session.commit()

        return UserYarnManager().convert_user_yarn_to_user_yarn_v1(user_yarn=user_yarn)


# `PUT /v1/users/{username}/yarns/{yarn_id}`

# `DELETE /v1/users/{username}/yarns/{yarn_id}`
