import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.user_yarn import UserYarnV1


logger = logging.getLogger(__name__)


class UserYarnManager:

    def convert_user_yarn_to_user_yarn_v1(self, user_yarn) -> UserYarnV1:
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
        )
