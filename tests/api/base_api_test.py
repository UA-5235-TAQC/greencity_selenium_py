import allure
from allure_commons.types import Severity
from clients.own_security_client import OwnSecurityClient
from data.config import Config
from schemas.greencity_user.own_security import success_sign_in_schema
from tests.utils.validators import validate_json


@allure.epic("User API")
@allure.feature("Authentication")
@allure.story("User Sign In")
@allure.title("Verify user can sign in and receive access token")
@allure.tag("Auth API")
@allure.severity(Severity.CRITICAL)
def test_api_is_work():
    """Verify that the user authentication API works correctly."""
    client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    response = client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
    print(response.json())
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    is_valid, error = validate_json(response.json(), success_sign_in_schema)
    assert is_valid, f"Response JSON does not match the expected schema: {error}"
    assert len(response.json()["accessToken"]) > 1, "Access token is empty"
    assert response.json()["userId"] == Config.USER_ID, "UserId does not match expected value"
    assert response.json()["name"] == Config.USER_NAME, "Name does not match expected value"
