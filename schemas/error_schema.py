error_response_schema = {
    "type": "object",
    "properties": {
        "timestamp": {"type": "string"},
        "status": {"type": "integer"},
        "error": {"type": "string"},
        "message": {"type": "string"},
        "path": {"type": "string"}
    },
    "required": ["timestamp", "status", "error", "path"],
    "additionalProperties": False
}
