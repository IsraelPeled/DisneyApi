from pydantic import BaseModel
from typing import Optional

class CharacterModel(BaseModel):
    id: int
    name: str
    film: str
    imageUrl: str
    score: int

class CreateCharacterModel(BaseModel):
    name: str
    film: str
    imageUrl: str
    score: int

class UpdateCharacterModel(BaseModel):
    name: Optional[str]
    film: Optional[str]
    imageUrl: Optional[str]
    score: int

class ScoreUpdate(BaseModel):
    score: int