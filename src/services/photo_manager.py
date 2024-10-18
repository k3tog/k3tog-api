import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.photo import PhotoInfoV1

logger = logging.getLogger(__name__)


class PhotoManager:

    @staticmethod
    def convert_photo_to_photo_info_v1(photo, signed_photo_url=None) -> PhotoInfoV1:
        return PhotoInfoV1(
            id=photo.id,
            photo_id=photo.photo_id,
            photo_key=photo.photo_key,
            signed_photo_url=signed_photo_url,
            is_thumbnail=photo.is_thumbnail,
            created_ts=convert_datetime_to_unixtime(photo.created_ts),
            type=photo.type,
        )
