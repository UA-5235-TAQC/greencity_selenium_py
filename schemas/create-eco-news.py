eco_news_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "shortInfo": {"type": "string"},
        "author": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        },
        "creationDate": {"type": "string", "format": "date-time"},
        "imagePath": {"type": ["string", "null"]},
        "source": {"type": ["string", "null"]},
        "tagsUk": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tagsEn": {
            "type": "array",
            "items": {"type": "string"}
        },
        "likes": {"type": "integer"},
        "countComments": {"type": "integer"},
        "countOfEcoNews": {"type": "integer"},
        "favorite": {"type": "boolean"}
    },
    "required": ["id", "title", "content", "author", "creationDate"],
    "additionalProperties": False
}