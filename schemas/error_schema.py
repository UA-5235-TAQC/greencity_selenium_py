error_response_schema = {
    "type": "object",
    "properties": {
        "name": {"type": ["string", "null"]},
        "timestamp": {"type": "string"},
        "status": {"type": "integer"},
        "error": {"type": "string"},
        "message": {"type": "string"},
        "path": {"type": "string"}
    },
    "required": ["message"],
    "additionalProperties": False
}
