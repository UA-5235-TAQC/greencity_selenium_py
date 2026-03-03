success_sign_in_schema = {
    "title": "SuccessSignInDto",
    "type": "object",
    "properties": {
        "userId": {
            "type": "integer",
            "format": "int64"
        },
        "accessToken": {
            "type": "string",
            "description": "JWT access token",
            "pattern": "^[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+\\.?[A-Za-z0-9-_.+/=]*$"
        },
        "refreshToken": {
            "type": "string",
            "description": "JWT refresh token",
            "pattern": "^[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+\\.?[A-Za-z0-9-_.+/=]*$"
        },
        "name": {
            "type": "string"
        },
        "ownRegistrations": {
            "type": "boolean"
        }
    },
    "required": ["userId", "accessToken", "refreshToken", "name", "ownRegistrations"],
    "additionalProperties": False
}