from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from configuration import collection
from src.database.schemas import all_characters, individual_data
from src.database.models import CharacterModel, UpdateCharacterModel, ScoreUpdate
import random

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
    #return {'message': 'hi'}

@router.get("/{character_id}")
async def get_charater_by_id(character_id: int):
    data = collection.find_one({"id": character_id})
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return individual_data(data)


@router.post("/")
async def create_character(new_character: CharacterModel):
    try:
        resp = collection.insert_one(dict(new_character))
        return {"stauts_code":200, "id": str(resp.inserted_id), "data": new_character}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error accured {e}")


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
        # Find the character to ensure it exists
        result = collection.find_one({"id": character_id})
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

        # Delete the character
        delete_result = collection.delete_one({"id": character_id})
        
        # Confirm deletion
        if delete_result.deleted_count == 1:
            return {"status_code": 204, "message": "Character deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Some error occurred: {e}")