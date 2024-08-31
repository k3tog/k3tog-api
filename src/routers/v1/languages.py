import logging
from typing import List

from fastapi import APIRouter

from routers.utils import APITags
from schemas.v1.language import LanguageV1
from db.database import get_db_session
from models.language import Language
from services.language_manager import LanguageManager


logger = logging.getLogger(__name__)

router = APIRouter()


# `GET /v1/languages/`
@router.get(
    "/languages/",
    tags=[APITags.languages],
    description="Get a list of supporting languages",
    response_model=List[LanguageV1],
    response_model_exclude_none=True,
)
async def get_languages():
    with get_db_session() as session:
        # fetch all supporting languages
        languages = Language.get_languages(session=session)

        language_infos = []
        language_manager = LanguageManager()
        for language in languages:
            language_infos.append(
                language_manager.convert_language_to_language_v1(language=language)
            )

    return language_infos
