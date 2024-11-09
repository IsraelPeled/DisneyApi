from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from configuration import collection
from src.database.schemas import all_characters, individual_data
from src.database.models import CreateCharacterModel, UpdateCharacterModel, ScoreUpdate
import random
from bson import ObjectId  # Import ObjectId to check and handle it
from fastapi.encoders import jsonable_encoder

def convert_objectid(data):
    """Recursively convert ObjectId fields to strings in a dictionary."""
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

router = APIRouter()

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

@router.get("/{character_id}")
async def get_charater_by_id(character_id: int):
    data = collection.find_one({"id": character_id})
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return individual_data(data)

@router.post("/")
async def create_character(new_character: CreateCharacterModel):
    try:
        # Find the highest existing `id` in the collection and increment by 1
        last_character = collection.find_one(sort=[("id", -1)])
        new_id = last_character["id"] + 1 if last_character else 0  # Start with `id` 1 if the collection is empty
        
        # Merge `id` with the other character data
        character_data = {"id": new_id, **new_character.dict()}
        
        # Insert the character into the collection
        resp = collection.insert_one(character_data)
        
        # Convert _id (inserted_id) and other ObjectId fields to string
        character_data["_id"] = str(resp.inserted_id)
        character_data = convert_objectid(character_data)  # Convert any ObjectId fields
        
        # Return JSON-serializable data
        return {
            "status_code": 200,
            "id": str(resp.inserted_id),
            "data": character_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error occurred: {e}")
    
@router.put("/{character_id}")
async def updated_character(character_id: int, updated_data: UpdateCharacterModel):
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
    
#TODO: update_score function
@router.put("/score/{character_id}")
async def update_character_score(character_id: int, score_update: ScoreUpdate):
    try:
        # Find the character to ensure it exists
        existing_character = collection.find_one({"id": character_id})
        if not existing_character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

        # Update only the score field
        update_result = collection.update_one(
            {"id": character_id},
            {"$set": {"score": score_update.score}}
        )

        # Confirm update
        if update_result.modified_count == 1:
            return {"status_code": 200, "message": "Score updated successfully"}
        else:
            return {"status_code": 200, "message": "Score is already up to date"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error occurred: {e}")


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(character_id: int):
    try:
        result = collection.find_one({"id": character_id})
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

        delete_result = collection.delete_one({"id": character_id})
        
        if delete_result.deleted_count == 1:
            return {"status_code": 204, "message": "Character deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error occurred: {e}")