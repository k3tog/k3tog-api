import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_yarn import UserYarnV1
from services.photo_manager import PhotoManager
from services.storage_manager import StorageManager


logger = logging.getLogger(__name__)


class UserYarnManager:

    def convert_user_yarn_to_user_yarn_v1(self, user_yarn, photos=[]) -> UserYarnV1:
        photo_manager = PhotoManager()

        photo_info_list = []
        if photos:
            storage_manager = StorageManager()
            for photo in photos:
                signed_photo_url = storage_manager.generate_signed_url(
                    category="photos", photo_key=photo.photo_key
                )
                photo_info_list.append(
                    photo_manager.convert_photo_to_photo_info_v1(
                        photo, signed_photo_url
                    )
                )
        return UserYarnV1(
            id=user_yarn.id,
            yarn_name=user_yarn.yarn_name,
            brand_name=user_yarn.brand_name,
            color=user_yarn.color,
            needle_range=(user_yarn.needle_range.lower, user_yarn.needle_range.upper),
            hook_range=(user_yarn.hook_range.lower, user_yarn.hook_range.upper),
            weight=user_yarn.weight,
            note=user_yarn.note,
            created_ts=convert_datetime_to_unixtime(user_yarn.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_yarn.updated_ts),
            photos=photo_info_list,
        )
