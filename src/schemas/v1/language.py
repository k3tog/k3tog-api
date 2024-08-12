from pydantic import BaseModel


class LanguageV1(BaseModel):
    id: int
    name: str
