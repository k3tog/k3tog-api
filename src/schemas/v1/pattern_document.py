from pydantic import BaseModel


class PatternDocumentV1(BaseModel):
    id: int
    document_id: str
    document_key: str
    filename_display: str
    created_ts: int
    # TODO(irene): add signed url
