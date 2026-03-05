eco_news_tags_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "name", "languageCode"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "languageCode": {"type": ["string", "null"]}
        }
    }
}