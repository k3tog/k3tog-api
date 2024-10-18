import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_needle import UserNeedleV1
from services.photo_manager import PhotoManager
from schemas.v1.user_gauge import UserGaugeV1
from services.storage_manager import StorageManager

logger = logging.getLogger(__name__)


class UserGaugeManager:

    def convert_user_gauge_to_user_gauge_v1(
        self, user_gauge, photo=None
    ) -> UserNeedleV1:
        photo_manager = PhotoManager()

        signed_photo_url = None
        if photo:
            storage_manager = StorageManager()
            signed_photo_url = storage_manager.generate_signed_url(
                category="photos", photo_key=photo.photo_key
            )
        photo = (
            photo_manager.convert_photo_to_photo_info_v1(photo, signed_photo_url)
            if photo
            else None
        )

        return UserGaugeV1(
            id=user_gauge.id,
            yarn_description=user_gauge.yarn_description,
            needle_size=user_gauge.needle_size,
            stitches=user_gauge.stitches,
            rows=user_gauge.rows,
            note=user_gauge.note,
            created_ts=convert_datetime_to_unixtime(user_gauge.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_gauge.updated_ts),
            photo=photo,
        )
