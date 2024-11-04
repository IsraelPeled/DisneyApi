def individual_data(character):
    return {
        "id": character["id"],
        "name": character["name"],
        "film": character["film"],
        "imageUrl": character["imageUrl"],
        "score": character["score"]
    }

def all_characters(characters):
    return [individual_data(character) for character in characters]