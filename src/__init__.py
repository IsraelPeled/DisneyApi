from fastapi import FastAPI
from src.characters.routers import router
from src.characters.root import root_route
from fastapi.middleware.cors import CORSMiddleware
from middleware import register_middleware


version="v1"

app = FastAPI(
    title= "DisneyAPI",
    description= "A REST API of Disney characters information.",
    version= version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact={
        "name": "Israel Peled",
        "email": "israelpeled3@gmail.com",
        "url": "https://github.com/IsraelPeled/DisneyApi"
    },
    openapi_url=f"/api/{version}/openapi.json"
    
)

register_middleware(app)

app.include_router(router=root_route, prefix=f"/api/{version}/root", tags=["root"])
app.include_router(router=router, prefix=f"/api/{version}/characters", tags=["characters"])