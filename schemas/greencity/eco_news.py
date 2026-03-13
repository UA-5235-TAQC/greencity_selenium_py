from schemas.author import author_response_schema
from schemas.greencity.eco_news_tags_schema import tag_response_schema

eco_news_response_schema = {
    "title": "EcoNewsResponse",
    "type": "object",
    "properties": {
        "id": {"type": "integer", "description": "Unique identifier of the EcoNews item"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "shortInfo": {"type": ["string", "null"]},
        "author": author_response_schema,
        "creationDate": {"type": "string", "format": "date-time"},
        "imagePath": {"type": ["string", "null"]},
        "source": {"type": ["string", "null"]},
        "tagsUk": {
            "type": "array",
            "items": tag_response_schema["properties"]["name"]
        },
        "tagsEn": {
            "type": "array",
            "items": tag_response_schema["properties"]["name"]
        },
        "likes": {"type": "integer"},
        "countComments": {"type": "integer"},
        "countOfEcoNews": {"type": "integer", "default": 1},
        "favorite": {"type": "boolean"},
        "dislikes": {"type": "integer", "default": 0},
        "hidden": {"type": "boolean", "default": False}
    },
    "required": [
        "id", "title", "content", "shortInfo", "author",
        "creationDate", "imagePath", "tagsUk", "tagsEn",
        "likes", "countComments"
    ],
    "additionalProperties": False
}

eco_news_page_schema = {
    "title": "EcoNewsPageResponse",
    "type": "object",
    "definitions": {
        "EcoNewsResponse": eco_news_response_schema
    },
    "properties": {
        "page": {
            "type": "array",
            "items": {"$ref": "#/definitions/EcoNewsResponse"}
        },
        "totalElements": {"type": "integer"},
        "currentPage": {"type": "integer"},
        "totalPages": {"type": "integer"},
        "number": {"type": "integer"},
        "hasPrevious": {"type": "boolean"},
        "hasNext": {"type": "boolean"},
        "first": {"type": "boolean"},
        "last": {"type": "boolean"}
    },
    "required": [
        "page", "totalElements", "currentPage", "totalPages",
        "number", "hasPrevious", "hasNext", "first", "last"
    ],
    "additionalProperties": False
}
