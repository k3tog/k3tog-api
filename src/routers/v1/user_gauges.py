import logging
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, status

from schemas.v1.user_gauge import UserGaugeCreateRequestInfoV1, UserGaugeV1
from routers.utils import APITags
from db.database import get_db_session
from models.photo import Photo
from models.user import User
from models.user_gauge import UserGauge
from services.user_gauge_manager import UserGaugeManager


logger = logging.getLogger(__name__)

router = APIRouter()


# `GET /v1/users/{username}/gauges/`


# `GET /v1/users/{username}/gauges/{gauge_id}`


# `POST /v1/users/{username}/gauges/`
@router.post(
    "/v1/users/{username}/gauges/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.gauges],
    description="Create a new needle for the user",
    response_model=UserGaugeV1,
    response_model_exclude_none=True,
)
async def create_user_gauge(
    gauge_create_req: UserGaugeCreateRequestInfoV1,
    username: Annotated[
        str, Path(title="Username of the user to create a new gauge for")
    ],
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        # if photo id was sent
        # find the photo db row by photo id
        photo = Photo.get_photo_by_photo_id(
            session=session, photo_id=gauge_create_req.photo_id
        )

        user_gauge = UserGauge(
            yarn_description=gauge_create_req.yarn_description,
            needle_size=gauge_create_req.needle_size,
            stitches=gauge_create_req.stitches,
            rows=gauge_create_req.rows,
            note=gauge_create_req.note,
            user_id=user.id,
            yarn_id=gauge_create_req.yarn_id,
        )

        session.add(user_gauge)
        session.flush()

        if photo:
            photo.reference_id = user_gauge.id
            photo.type = "user_gauge"

        session.commit()

        return UserGaugeManager().convert_user_gauge_to_user_gauge_v1(
            user_gauge=user_gauge, photo=photo
        )


# `PUT /v1/users/{username}/gauges/{gauge_id}`

# `DELETE /v1/users/{username}/gauges/{gauge_id}`
