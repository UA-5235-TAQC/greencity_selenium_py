get_comment_by_id_response_schema = {
    "title": "CommentFullDto",
    "type": "object",
    "properties": {
        "id": { "type": "integer" },
        "createdDate": { 
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}" 
        },
        "modifiedDate": { 
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}" 
        },
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
        "parentCommentId": { "type": ["integer", "null"] },
        "text": { "type": "string" },
        "replies": { "type": "integer", "minimum": 0 },
        "likes": { "type": "integer", "minimum": 0 },
        "dislikes": { "type": "integer", "minimum": 0 },
        "currentUserLiked": { "type": "boolean" },
        "currentUserDisliked": { "type": "boolean" },
        "status": { 
            "type": "string",
            "enum": ["ORIGINAL", "EDITED", "DELETED", "HIDDEN"]
        },
        "additionalImages": {
            "type": "array",
            "items": { "type": "string" }
        }
    },
    "required": [
        "id", "createdDate", "modifiedDate", "author", "parentCommentId", 
        "text", "replies", "likes", "dislikes", "currentUserLiked", 
        "currentUserDisliked", "status", "additionalImages"
    ],
    "additionalProperties": False
}