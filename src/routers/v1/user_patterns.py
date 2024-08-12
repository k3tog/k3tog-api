import logging

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status

from routers.utils import APITags
from schemas.v1.user_pattern import UserPatternCreateRequestInfoV1, UserPatternV1
from db.database import get_db_session
from models.user import User
from models.user_pattern import UserPattern
from src.services.user_pattern_manager import UserPatternManager

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/{username}/patterns/`
@router.get(
    "/v1/users/{username}/patterns/",
    tags=[APITags.patterns],
    description="Get a list of patterns for the user",
    response_model=List[UserPatternV1],
    response_model_exclude_none=True,
)
async def get_user_patterns(
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

        # fetch all patterns that the user owns
        user_patterns = UserPattern.get_user_patterns_by_user_id(
            session=session, user_id=user.id
        )

    user_pattern_info = []
    user_pattern_manager = UserPatternManager()
    for user_pattern in user_patterns:
        user_pattern_info.append(
            user_pattern_manager.convert_user_pattern_to_user_pattern_v1(
                user_pattern=user_pattern
            )
        )

    return user_pattern_info


# `GET /v1/users/{username}/patterns/{pattern_id}`
@router.get(
    "/v1/users/{username}/patterns/{pattern_id}",
    tags=[APITags.patterns],
    description="Get a single pattern for the user",
    response_model=UserPatternV1,
    response_model_exclude_none=True,
)
async def get_user_pattern(
    username: Annotated[
        str, Path(title="Username of the user to get a list of patterns for")
    ],
    pattern_id: Annotated[int, Path(title="ID of the pattern")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_pattern = UserPattern.get_user_pattern_by_pattern_id_user_id(
            session=session, pattern_id=pattern_id, user_id=user.id
        )

    if user_pattern:
        return UserPatternManager().convert_user_pattern_to_user_pattern_v1(
            user_pattern=user_pattern
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No pattern found"
    )


# `POST /v1/users/{username}/patterns/`
@router.post(
    "/v1/users/{username}/patterns/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.patterns],
    description="Create a new pattern for the user",
    response_model=UserPatternV1,
    response_model_exclude_none=True,
)
async def create_user_pattern(
    pattern_create_req: UserPatternCreateRequestInfoV1,
    username: Annotated[
        str, Path(title="Username of the user to create a new project for")
    ],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_pattern = UserPattern(
            name=pattern_create_req.name,
            author=pattern_create_req.author,
            # TODO(irene): file_attachment
            user_id=user.id,
        )

        session.add(user_pattern)
        session.commit()

    return UserPatternManager().convert_user_pattern_to_user_pattern_v1(
        user_pattern=user_pattern
    )


# `PUT /v1/users/{username}/patterns/{pattern_id}`

# `DELETE /v1/users/{username}/patterns/{pattern_id}`
