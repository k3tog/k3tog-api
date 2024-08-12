import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_needle import UserNeedleV1

logger = logging.getLogger(__name__)


class UserNeedleManager:
    def convert_user_needle_to_user_needle_v1(self, user_needle) -> UserNeedleV1:
        return UserNeedleV1(
            id=user_needle.id,
            name=user_needle.name,
            size=user_needle.size,
            note=user_needle.note,
            created_ts=convert_datetime_to_unixtime(user_needle.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_needle.updated_ts),
        )
