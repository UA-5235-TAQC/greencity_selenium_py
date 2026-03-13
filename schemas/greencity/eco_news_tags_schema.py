tag_response_schema = {
    "id": "integer",
    "title": "TagResponse",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "languageCode": {"type": ["string", "null"]}
    },
    "required": ["name"],
    "additionalProperties": False
}

eco_news_tags_schema = {
    "type": "array",
    "items": tag_response_schema
}
