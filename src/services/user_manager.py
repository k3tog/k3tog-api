import logging

from schemas.v1.user import UserV1
from services.utils import convert_datetime_to_unixtime

logger = logging.getLogger()


class UserManager:
    def convert_user_to_user_v1(self, user):
        location_str = f"{user.location_state}, {user.location_country}"

        return UserV1(
            id=user.id,
            external_id=user.external_id,
            username=user.username,
            email=user.email,
            location=(
                location_str if user.location_state and user.location_country else None
            ),
            birthday=user.birthday.strftime("%B %d, %Y") if user.birthday else None,
            knitting_sice=(
                f"Since {user.knitting_since}" if user.knitting_since else None
            ),
            bio=user.bio,
            avatar_url=user.avatar_url,
            preferred_language=user.preferred_language.name,
            created_ts=convert_datetime_to_unixtime(user.created_ts),
            updated_ts=convert_datetime_to_unixtime(user.updated_ts),
            deactivated_ts=convert_datetime_to_unixtime(user.deactivated_ts),
        )
