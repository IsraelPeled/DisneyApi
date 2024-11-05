from fastapi import FastAPI
from src.characters.routers import router


version="v1"

app = FastAPI(
    title="DisneyAPI",
    description="A REST API of Disney characters information.",
    version= version
    
)

app.include_router(router=router, prefix=f'/api/{version}/characters', tags=["characters"])