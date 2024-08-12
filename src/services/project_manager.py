import logging

from services.utils import convert_datetime_to_unixtime
from schemas.v1.project import ProjectV1
from schemas.v1.user_pattern import UserPatternV1
from services.user_yarn_manager import UserYarnManager
from services.user_needle_manager import UserNeedleManager

logger = logging.getLogger(__name__)


class ProjectManager:

    def convert_project_to_project_v1(self, project) -> ProjectV1:
        user_yarns = []
        user_yarn_manager = UserYarnManager()
        for user_yarn in project.user_yarns:
            user_yarns.append(
                user_yarn_manager.convert_user_yarn_to_user_yarn_v1(user_yarn=user_yarn)
            )

        user_needles = []
        user_needle_manager = UserNeedleManager()
        for user_needle in project.user_needles:
            user_needles.append(
                user_needle_manager.convert_user_needle_to_user_needle_v1(
                    user_needle=user_needle
                )
            )

        return ProjectV1(
            id=project.id,
            title=project.title,
            status=project.status,
            co_date=project.co_date.strftime("%B %d, %Y") if project.co_date else None,
            fo_date=project.fo_date.strftime("%B %d, %Y") if project.fo_date else None,
            size=project.size,
            note=project.note,
            pattern=UserPatternV1(
                id=project.user_pattern.id,
                name=project.user_pattern.name,
                author=project.user_pattern.author,
                created_ts=convert_datetime_to_unixtime(
                    project.user_pattern.created_ts
                ),
                updated_ts=convert_datetime_to_unixtime(
                    project.user_pattern.updated_ts
                ),
            ),
            yarns=user_yarns,
            needles=user_needles,
        )
