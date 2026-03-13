from schemas.author import author_response_schema

comment_schema = {
    "title": "CommentDto",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "createdDate": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        },
        "modifiedDate": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        },
        "author": author_response_schema,
        "parentCommentId": {"type": ["integer", "null"]},
        "text": {"type": "string"},
        "replies": {"type": "integer", "minimum": 0},
        "likes": {"type": "integer", "minimum": 0},
        "dislikes": {"type": "integer", "minimum": 0},
        "currentUserLiked": {"type": "boolean"},
        "currentUserDisliked": {"type": "boolean"},
        "status": {
            "type": "string",
            "enum": ["ORIGINAL", "EDITED", "DELETED", "HIDDEN"],
            "default": "ORIGINAL"
        },
        "additionalImages": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["id", "author", "text", "createdDate", "additionalImages"],
    "additionalProperties": False
}

comment_page_response_schema = {
    "title": "GetCommentPageResponse",
    "type": "object",
    "properties": {
        "page": {
            "type": "array",
            "items": comment_schema
        },
        "totalElements": {
            "type": "integer"
        },
        "currentPage": {
            "type": "integer"
        },
        "totalPages": {
            "type": "integer"
        }
    },
    "required": [
        "page",
        "totalElements",
        "currentPage",
        "totalPages"
    ],
    "additionalProperties": False
}
