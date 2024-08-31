from typing import List, Optional
from pydantic import BaseModel


class PatternDocumentInfoV1(BaseModel):
    id: int
    document_id: str
    document_key: str
    filename_display: str
    created_ts: int
