comment_creation_schema = {
    "title": "CommentCreatedDto",
    "type": "object",
    "properties": {
        "id": { "type": "integer" },
        "author": {
            "type": "object",
            "properties": {
                "id": { "type": "integer" },
                "name": { "type": "string" },
                "profilePicturePath": { "type": ["string", "null"] }
            },
            "required": ["id", "name", "profilePicturePath"],
            "additionalProperties": False
        },
        "text": { "type": "string" },
        "createdDate": { 
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}" 
        },
        "additionalImages": {
            "type": "array",
            "items": { "type": "string" }
        }
    },
    "required": ["id", "author", "text", "createdDate", "additionalImages"],
    "additionalProperties": False
}