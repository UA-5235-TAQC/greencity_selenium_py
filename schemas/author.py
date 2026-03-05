author_response_schema = {
    "$id": "https://example.com/schemas/author_response.json",
    "title": "AuthorResponse",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "profilePicturePath": {"type": "string", "default": ""}
    },
    "required": ["id", "name"],
    "additionalProperties": False
}
