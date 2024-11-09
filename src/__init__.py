from fastapi import FastAPI
from src.characters.routers import router
from fastapi.middleware.cors import CORSMiddleware


version="v1"

allow_origins=["http://127.0.0.1:8000", "http://0.0.0.0:8000"]

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

#TODO: ADDING CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Allows all origins, can be replaced with specific URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router=router, prefix=f"/api/{version}/characters", tags=["characters"])