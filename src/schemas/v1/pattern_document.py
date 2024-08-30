from typing import List, Optional
from pydantic import BaseModel

class PatternDocumentV1(BaseModel):
    id: int
    file_reference: str # could be url 
    filename_display: str
    created_ts: int 
    
