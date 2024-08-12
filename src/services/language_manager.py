import logging

from schemas.v1.language import LanguageV1

logger = logging.getLogger(__name__)


class LanguageManager:

    def convert_language_to_language_v1(self, language) -> LanguageV1:
        return LanguageV1(id=language.id, name=language.name)
