from typing import List, Optional
from pydantic import BaseModel

from schemas.v1.pattern_document import PatternDocumentV1


class UserPatternV1(BaseModel):
    id: int
    name: str
    author: Optional[str]
    description: Optional[str]
    created_ts: int
    updated_ts: int
    pattern_documents: Optional[List[PatternDocumentV1]]


class UserPatternCreateRequestInfoV1(BaseModel):
    name: str
    author: Optional[str]
    description: Optional[str]
    pattern_document_id: Optional[str]
