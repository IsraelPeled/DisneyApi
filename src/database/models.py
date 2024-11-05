from pydantic import BaseModel


class Character(BaseModel):
    id: int
    name: str
    film: str
    imageUrl: str
    score: int