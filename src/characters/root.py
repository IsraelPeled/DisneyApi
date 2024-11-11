from fastapi import APIRouter

root_route = APIRouter()

@root_route.get('/')
async def reed_root():
    return {"message": "working"}