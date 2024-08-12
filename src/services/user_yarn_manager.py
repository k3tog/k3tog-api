import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_yarn import UserYarnV1


logger = logging.getLogger(__name__)


class UserYarnManager:

    def convert_user_yarn_to_user_yarn_v1(self, user_yarn):
        return UserYarnV1(
            id=user_yarn.id,
            name=user_yarn.name,
            color=user_yarn.color,
            none=user_yarn.note,
            num_used=user_yarn.num_used,
            created_ts=convert_datetime_to_unixtime(user_yarn.created_ts),
            updated_ts=convert_datetime_to_unixtime(user_yarn.updated_ts),
        )
