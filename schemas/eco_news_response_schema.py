eco_news_item_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "shortInfo": {"type": ["string", "null"]},
        "author": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        },
        "creationDate": {"type": "string"},
        "imagePath": {"type": ["string", "null"]},
        "source": {"type": ["string", "null"]},
        "tagsUk": {"type": "array", "items": {"type": "string"}},
        "tagsEn": {"type": "array", "items": {"type": "string"}},
        "likes": {"type": "integer"},
        "countComments": {"type": "integer"},
        "countOfEcoNews": {"type": "integer"},
        "favorite": {"type": "boolean"}
    },
    "required": ["id", "title", "content", "author", "creationDate"],
    "additionalProperties": False
}

eco_news_page_schema = {
    "type": "object",
    "properties": {
        "page": {
            "type": "array",
            "items": eco_news_item_schema
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
    "required": ["page", "totalElements", "currentPage", "totalPages"],
    "additionalProperties": False
}
