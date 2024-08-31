import logging
import uuid
import os

from services.storage_manager import StorageManager
from schemas.v1.pattern_document import PatternDocumentInfoV1
from services.utils import convert_datetime_to_unixtime

logger = logging.getLogger(__name__)


class PatternDocumentManager:

    def upload_pattern_attachment_to_storage(self, filepath, username, content_type):
        unique_filepath = f"{username}/{str(uuid.uuid4())}_{os.path.basename(filepath)}"

        return StorageManager().upload_single_attachment(
            filepath=filepath,
            target_path=unique_filepath,
            category="patterns",
            content_type=content_type,
        )

    def convert_pattern_document_to_pattern_document_info_v1(
        self, pattern_document
    ) -> PatternDocumentInfoV1:

        return PatternDocumentInfoV1(
            id=pattern_document.id,
            document_id=pattern_document.document_id,
            document_key=pattern_document.document_key,
            filename_display=pattern_document.filename_display,
            created_ts=convert_datetime_to_unixtime(pattern_document.created_ts),
        )
