from fastapi import FastAPI, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from configuration import collection
from database.models import Character
from database.schemas import all_characters, individual_data
from bson.objectid import ObjectId
import random

app = FastAPI()
router = APIRouter()

#TODO: CORSMiddleware

@router.get("/random")
async def get_random_character():
    data = list(collection.find()) 
    if not data:
        raise HTTPException(status_code=404, detail="No characters found")
    
    random_character = random.choice(data)  
    return individual_data(random_character)


@router.get("/")
async def get_all_charaters():
    data = collection.find()
    return all_characters(data)
    #return {'message': 'hi'}

@router.get("/{character_id}")
async def get_charater_by_id(character_id: int):
    data = collection.find_one({"id": character_id})
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return individual_data(data)


@router.post("/")
async def create_character(new_character: Character):
    try:
        resp = collection.insert_one(dict(new_character))
        return {"stauts_code":200, "id": str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error accured {e}")

#TODO: update_score function
@router.put("/{character_id}")
async def updated_character(character_id: int, updated_data: Character):
    try:
        existing_doc = collection.find_one({"id": character_id})
        if not existing_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
        
        resp = collection.update_one(
            {"id": character_id},  # Use character_id here
            {"$set": dict(updated_data)}
        )
        return {"status_code": 200, "message": "Character updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error occurred: {e}")
    

app.include_router(router)