import logging

from typing import Annotated, List
import uuid
from fastapi import APIRouter, File, HTTPException, Path, UploadFile, status

from routers.utils import APITags
from db.database import get_db_session
from models.user import User
from services.storage_manager import (
    StorageManager,
    SupabaseStorageFileUploadFailedException,
)
from services.photo_manager import PhotoManager
from models.photo import Photo
from schemas.v1.photo import PhotoInfoV1

logger = logging.getLogger(__name__)


router = APIRouter()


# `POST /v1/users/{username}/photos/`
@router.post(
    "/v1/users/{username}/photos/",
    status_code=status.HTTP_201_CREATED,
    tags=[APITags.photos],
    description="Upload multiple photos to the file storage",
    response_model=List[PhotoInfoV1],
    response_model_exclude_none=True
)
async def upload_photo_attachments(
    username: Annotated[
        str, Path(title="Username of the user to create a new pattern for")
    ],
    photos: List[UploadFile] = File(...),
    category: str = "project",  # TODO(irene): change to Enum - user_yarn, user_needle, project, user_gauge
):
    with get_db_session() as session:
        user = User.get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )

        # TODO(irene): need to verify if the file was image?

        storage_manager = StorageManager()
        added_photo_keys = []
        db_added_photos = []
        for photo in photos:
            tmp_filepath = f"/tmp/{photo.filename}"
            with open(tmp_filepath, "wb") as f:
                f.write(await photo.read())

            unique_filepath = f"{username}/{category}/{str(uuid.uuid4())}_{photo.filename}"

            try:
                photo_id, photo_key = storage_manager.upload_single_attachment(
                    filepath=tmp_filepath,
                    target_path=unique_filepath,
                    category="photos",
                    content_type=photo.headers.get("content-type"),
                )
                added_photo_keys.append(photo_key)

            except SupabaseStorageFileUploadFailedException:
                # TODO(irene): remove added photos from the storage
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Uploading photo attachments failed. Please try again.",
                )

            photo_row = Photo(
                photo_id=photo_id, photo_key=photo_key, is_thumbnail=False, type=category
            )
            session.add(photo_row)
            db_added_photos.append(photo_row)

        session.commit()

        photo_manager = PhotoManager()

        return [
            photo_manager.convert_photo_to_photo_info_v1(photo)
            for photo in db_added_photos
        ]
