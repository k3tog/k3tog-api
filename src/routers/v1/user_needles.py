import logging
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, status

from db.database import get_db_session
from models.photo import Photo
from models.user import User
from models.user_needle import UserNeedle
from routers.utils import APITags
from schemas.v1.user_needle import UserNeedleCreateRequestInfoV1, UserNeedleV1
from services.user_needle_manager import UserNeedleManager

logger = logging.getLogger(__name__)


router = APIRouter()


# `GET /v1/users/{username}/needles/`
@router.get(
    "/v1/users/{username}/needles/",
    tags=[APITags.needles],
    description="Get a list of needles for the user",
    response_model=List[UserNeedleV1],
    response_model_exclude_none=True,
)
async def get_user_needles(
    username: Annotated[
        str, Path(title="Username of the user to get a list of needles for")
    ]
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_needles = UserNeedle.get_user_needles_by_user_id(
            session=session, user_id=user.id
        )

        user_needle_info = []
        user_needle_manager = UserNeedleManager()
        for user_needle in user_needles:
            # get photos for the user needle
            photos = Photo.get_photos_by_reference_id_type(
                session=session, reference_id=user_needle.id, type="user_needle"
            )
            user_needle_info.append(
                user_needle_manager.convert_user_needle_to_user_needle_v1(
                    user_needle=user_needle, photos=photos
                )
            )

    return user_needle_info


# `GET /v1/users/{username}/needles/{needle_id}`
@router.get(
    "/v1/users/{username}/needles/{needle_id}",
    tags=[APITags.needles],
    description="Get a single needle for the user",
    response_model=UserNeedleV1,
    response_model_exclude_none=True,
)
async def get_user_needle(
    username: Annotated[
        str, Path(title="Username of the user to get a list of needles for")
    ],
    needle_id: Annotated[int, Path(title="ID of the needle")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        user_needle = UserNeedle.get_user_needle_by_needle_id_user_id(
            session=session, needle_id=needle_id, user_id=user.id
        )

        if user_needle:
            # get photos for the user needle
            photos = Photo.get_photos_by_reference_id_type(
                session=session, reference_id=user_needle.id, type="user_needle"
            )
            return UserNeedleManager().convert_user_needle_to_user_needle_v1(
                user_needle=user_needle, photos=photos
            )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No needle found")


# `POST /v1/users/{username}/needles/`
@router.post(
    "/v1/users/{username}/needles/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.needles],
    description="Create a new needle for the user",
    response_model=UserNeedleV1,
    response_model_exclude_none=True,
)
async def create_user_needle(
    needle_create_req: UserNeedleCreateRequestInfoV1,
    username: Annotated[
        str, Path(title="Username of the user to create a new needle for")
    ],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        # if photo ids were sent
        # find the photo db rows by photo ids
        photos = Photo.get_photos_by_photo_ids(
            session=session, photo_ids=needle_create_req.photo_ids
        )

        user_needle = UserNeedle(
            name=needle_create_req.name,
            size=needle_create_req.size,
            note=needle_create_req.note,
            user_id=user.id,
        )
        session.add(user_needle)
        session.flush()

        for photo in photos:
            photo.reference_id = user_needle.id
            photo.type = "user_needle"

        session.commit()

        return UserNeedleManager().convert_user_needle_to_user_needle_v1(
            user_needle=user_needle, photos=photos
        )


# `PUT /v1/users/{username}/needles/{needle_id}`


# `DELETE /v1/users/{username}/needles/{needle_id}`
@router.delete(
    "/v1/users/{username}/needles/{needle_id}",
    tags=[APITags.needles],
    description="Delete a needle for the user",
)
async def delete_user_needle(
    username: Annotated[str, Path(title="Username of the user to delete a needle for")],
    needle_id: Annotated[int, Path(title="ID of the needle to delete")],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        # delete the user needle and all connected photos
        user_needle = UserNeedle.delete_user_needle_by_needle_id_user_id(
            session=session, needle_id=needle_id, user_id=user.id
        )

        if user_needle:
            photos = Photo.delete_photos_by_reference_id_type(
                session=session, reference_id=needle_id, type="user_needle"
            )
            if photos:
                session.add_all(photos)

            session.add(user_needle)
            session.commit()

            return UserNeedleManager().convert_user_needle_to_user_needle_v1(
                user_needle=user_needle, photos=photos
            )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No needle found")
