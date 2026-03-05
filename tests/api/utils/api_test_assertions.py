from requests import Response

from tests.api.utils.error_response import ErrorResponse


def assert_bad_request(response: Response, expected_message: str):
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
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    json_data = response.json()
    error = ErrorResponse(**json_data)
    assert error.error == "Unauthorized", f"Error message should match expected, got {error.error}"


def assert_error_message(response: Response, expected_message: str):
    """Asserts that the error message in the response matches the expected message."""
    json_data = response.json()
    error = ErrorResponse(**json_data)
    assert error.message == expected_message, (
        f"Error message should match expected, got {error.message}"
    )
