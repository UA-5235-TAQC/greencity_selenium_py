from typing import Union, List
from jsonschema.validators import validate
from requests import Response

from schemas.error_schema import error_response_schema


def assert_bad_request(response: Response, expected_message: Union[str, List[str]]):
    """Asserts that the response is 400 Bad Request and the error message matches."""
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    assert_error_message(response, expected_message)


def assert_not_found(response: Response, expected_message: str):
    """Asserts that the response is 404 Not Found and the error message matches."""
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"
    assert_error_message(response, expected_message)


def assert_ok(response: Response):
    """Asserts that the response is 200 OK."""
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"


def assert_created(response: Response):
    """Asserts that the response is 201 Created."""
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"


def assert_unauthorized(response: Response):
    """Asserts that the response is 401 Unauthorized and the error message is 'Unauthorized'."""
    json_data = response.json()
    error_message = json_data.get("error")
    assert error_message == "Unauthorized", f"Error message should match expected, got {error_message}"


def assert_error_message(response: Response, expected_message: Union[str, List[str]]):
    """
    Asserts that the error message(s) in the response match the expected message(s).
    Supports a single message (str) or multiple messages (list of str).
    """
    json_data = response.json()

    if isinstance(json_data, list):
        for e in json_data:
            validate(instance=e, schema=error_response_schema)
        messages = [e.get("message") for e in json_data]
    else:
        validate(instance=json_data, schema=error_response_schema)
        messages = [json_data.get("message")]

    if isinstance(expected_message, str):
        expected_message = [expected_message]

    for msg in expected_message:
        assert msg in messages, f"Expected error message '{msg}' not found in response"
