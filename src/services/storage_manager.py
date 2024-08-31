import logging

from services import get_supabase_cli


logger = logging.getLogger(__name__)


class SupabaseStorageFileUploadFailedException(Exception):
    pass


class StorageManager:
    BUCKETS = {"patterns": "k3tog-patterns"}

    def __init__(self):
        self.supabase = get_supabase_cli()

    def upload_single_attachment(self, filepath, target_path, category, content_type):
        with open(filepath, "rb") as f:
            res = self.supabase.storage.from_(self.BUCKETS.get(category)).upload(
                file=filepath,
                path=target_path,
                file_options={"content-type": content_type},
            )

        if res.status_code == 200:
            # TODO(irene): need to get signed url?
            # returning json for now - Id and Key(filepath in the storage)
            res_body = res.json()
            return res_body.get("Id"), res_body.get("Key")
        else:
            logger.warning(
                f"[{__class__.__name__}] uploading a single attachment: {filepath} failed."
            )
            raise SupabaseStorageFileUploadFailedException(
                f"[{__class__.__name__}] uploading a single attachment: {filepath} failed."
            )
