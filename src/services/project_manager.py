import logging

from schemas.v1.project import ProjectV1
from services.user_yarn_manager import UserYarnManager
from services.user_needle_manager import UserNeedleManager
from services.user_pattern_manager import UserPatternManager
from services.storage_manager import StorageManager
from services.photo_manager import PhotoManager

logger = logging.getLogger(__name__)


class ProjectManager:

    def convert_project_to_project_v1(self, project) -> ProjectV1:
        photos = []
        if project.photos:
            photo_manager = PhotoManager()
            storage_manager = StorageManager()
            for photo in project.photos:
                signed_photo_url = storage_manager.generate_signed_url(
                    category="photos", photo_key=photo.photo_key
                )
                photos.append(
                    photo_manager.convert_photo_to_photo_info_v1(
                        photo, signed_photo_url
                    )
                )

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

        user_pattern = UserPatternManager().convert_user_pattern_to_user_pattern_v1(
            user_pattern=project.user_pattern
        )

        return ProjectV1(
            id=project.id,
            title=project.title,
            status=project.status,
            co_date=project.co_date.strftime("%B %d, %Y") if project.co_date else None,
            fo_date=project.fo_date.strftime("%B %d, %Y") if project.fo_date else None,
            size=project.size,
            note=project.note,
            pattern=user_pattern,
            yarns=user_yarns,
            needles=user_needles,
            photos=photos,
        )
