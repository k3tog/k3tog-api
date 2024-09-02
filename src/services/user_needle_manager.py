import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_needle import UserNeedleV1
from services.photo_manager import PhotoManager

logger = logging.getLogger(__name__)


class UserNeedleManager:
    def convert_user_needle_to_user_needle_v1(
        self, user_needle, photos=[]
    ) -> UserNeedleV1:
        photo_manager = PhotoManager()
        photos = [
            photo_manager.convert_photo_to_photo_info_v1(photo) for photo in photos
        ]
        return UserNeedleV1(
            id=user_needle.id,
            name=user_needle.name,
            size=user_needle.size,
            note=user_needle.note,
            created_ts=convert_datetime_to_unixtime(user_needle.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_needle.updated_ts),
            photos=photos,
        )
