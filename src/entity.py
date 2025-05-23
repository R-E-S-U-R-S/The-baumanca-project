from typing import Optional
from pydantic import BaseModel

class Set(BaseModel):
    id: str
    name: str
    parts_volume: int
    released: Optional[int] = ""
    theme: Optional[str] = ""
    image_link: Optional[str] = ""
    instruction_link: Optional[str] = ""

class SearchFilter(BaseModel):
    parts_volume: int

class UserData(BaseModel):
    login: str
    password: str



