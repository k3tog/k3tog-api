import logging

from schemas.v1.user_pattern import UserPatternV1
from services.utils import convert_datetime_to_unixtime


logger = logging.getLogger(__name__)


class UserPatternManager:

    def convert_user_pattern_to_user_pattern_v1(self, user_pattern):
        return UserPatternV1(
            id=user_pattern.id,
            name=user_pattern.name,
            author=user_pattern.author,
            created_ts=convert_datetime_to_unixtime(user_pattern.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_pattern.updated_ts),
        )
