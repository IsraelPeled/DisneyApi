import requests
from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("WEBSITE_URL")

'''
response = requests.get(ENDPOINT)
print(response)

data = response.json()
print(data)
'''

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_character():
    payload = new_character_payload()
    create_response = create_character(payload)
    assert create_response.status_code == 200

    data = create_response.json()
    #print(data)

    character_id = data["data"]["id"]
    get_character_response = get_character(character_id)
    
    assert get_character_response.status_code == 200
    get_character_data = get_character_response.json()
    assert get_character_data["name"] == payload["name"]
    assert get_character_data["id"] == payload["id"]
    #print(get_character_data)


def test_can_update_character():
    #create character
    payload = new_character_payload()
    create_character_response = create_character(payload)
    assert create_character_response.status_code == 200
    character_id = create_character_response.json()["data"]["id"]

    # update the character
    new_payload = new_character_payload(name="new name", film="new film", imageUrl="new imageUrl")
    update_character_response = update_character(character_id, new_payload)
    assert update_character_response.status_code == 200

    # get and validate the changes
    get_character_response = get_character(character_id)
    assert get_character_response.status_code == 200
    get_character_data = get_character_response.json()
    assert get_character_data["name"] == new_payload["name"]
    assert get_character_data["film"] == new_payload["film"]
    assert get_character_data["imageUrl"] == new_payload["imageUrl"]


def test_can_delete_character():
    #create a character
    payload = new_character_payload()
    create_character_response = create_character(payload)
    assert create_character_response.status_code == 200
    character_id = create_character_response.json()["data"]["id"]

    #Delete the character
    delete_character_response = delete_character(character_id)
    assert delete_character_response.status_code == 204

    #Get the Character, and check that it's not found
    get_character_response = get_character(character_id)
    print(get_character_response.status_code)
    assert get_character_response.status_code == 404


def create_character(payload: dict):
    return requests.post(ENDPOINT, json=payload)

def get_character(character_id: int):
    return requests.get(ENDPOINT + f"/{character_id}")

def update_character(character_id: int, payload: dict):
    return requests.put(ENDPOINT + f'/{character_id}', json=payload)

def delete_character(character_id: int):
    return requests.delete(ENDPOINT + f'/{character_id}')


def new_character_payload(id: int = 92, name: str = "string", film: str = "string", imageUrl: str = "string", score: int = 1400):
    payload = {
        "id": id,
        "name": name,
        "film": film,
        "imageUrl": imageUrl,
        "score": score
    }
    return payload