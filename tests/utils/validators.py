from jsonschema import validate, ValidationError


def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        error_msg = "JSON validation error: " + str(e)
        return False, error_msg