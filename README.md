# Disney API

This project is a simple API for managing Disney characters. The API allows you to perform CRUD operations (Create, Read, Update, Delete) on characters from Disney films. It uses FastAPI for the backend and MongoDB as the database.

## Features

- **Create a new character**: Add new Disney characters with details such as name, film, image URL, and score.
- **Retrieve character details**: Fetch information about a specific character or all characters.
- **Update character details**: Modify the attributes of a character.
- **Delete a character**: Remove a character from the database.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **MongoDB**: NoSQL database used to store character information.
- **Python**: Programming language used for the backend development.
- **JavaScript (Fetch API)**: For client-side requests to interact with the API.

## API Endpoints

### Create a Character

- **Endpoint**: `POST /api/v1/characters/`
- **Body**:
  ```json
  {
    "name": "string",
    "film": "string",
    "imageUrl": "string",
    "score": 0
  }
  ```
- **Response**:
  ```json
  {
    "status_code": 200,
    "id": "inserted_id",
    "data": {
      "name": "string",
      "film": "string",
      "imageUrl": "string",
      "score": 0
    }
  }
  ```

### Get All Characters

- **Endpoint**: `GET /api/v1/characters/`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "character_name",
      "film": "film_name",
      "imageUrl": "url_to_image",
      "score": 10
    },
    ...
  ]
  ```

### Get a Character by ID

- **Endpoint**: `GET /api/v1/characters/{id}`
- **Response**:
  ```json
  {
    "id": 1,
    "name": "character_name",
    "film": "film_name",
    "imageUrl": "url_to_image",
    "score": 10
  }
  ```

### Update a Character

- **Endpoint**: `PUT /api/v1/characters/{id}`
- **Body**:
  ```json
  {
    "name": "updated_name",
    "film": "updated_film",
    "imageUrl": "updated_url",
    "score": 8
  }
  ```
- **Response**:
  ```json
  {
    "status_code": 200,
    "data": {
      "name": "updated_name",
      "film": "updated_film",
      "imageUrl": "updated_url",
      "score": 8
    }
  }
  ```

### Delete a Character

- **Endpoint**: `DELETE /api/v1/characters/{id}`
- **Response**:
  ```json
  {
    "status_code": 200,
    "message": "Character deleted successfully"
  }
  ```
