from typing import Any

from pytest import fixture
import allure
from requests import Response

from clients.comments_client import CommentsClient
from clients.eco_new_client import EcoNewClient
from clients.eco_news_client import EcoNewsClient
from clients.own_security_client import OwnSecurityClient
from data.api_news_test_data import EcoNewsDtoFactory
from data.config import Config
from data.ui_news_test_data import NewsTestData
from enums.news_tag import EcoNewsTag
from models.eco_news_request import EcoNewsRequest
from schemas.greencity_user.own_security import success_sign_in_schema
from tests.api.utils.api_test_assertions import assert_ok, assert_created
from tests.utils.validators import validate_json


@fixture(scope="session")
def eco_news_setup():
    """Fixture to prepare EcoNews client and fetch first EcoNews item."""
    eco_news_client = EcoNewClient(Config.BASE_GREEN_CITY_API_URL, token=None)
    response = eco_news_client.get_eco_news({"page": 0, "size": 10})
    page_response = response.json()
    first_news = page_response["page"][0]
    eco_news_id = first_news["id"]
    return {
        "client": eco_news_client,
        "eco_news_id": eco_news_id
    }


@fixture(scope="session")
def auth_token():
    """Get auth token."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    assert_ok(login_response)

    token = login_response.json().get("accessToken")
    return token


@fixture(scope="module")
def created_eco_news_without_image(auth_token):
    """Create EcoNews and print it to console."""
    client = EcoNewClient(Config.BASE_GREEN_CITY_API_URL, token=auth_token)
    factory = EcoNewsDtoFactory(eco_news_id=0)
    news_dto: EcoNewsRequest = factory.create_news_uk()
    response = client.post_eco_news(news_dto)

    assert_created(response)

    created_news = response.json()

    return {
        "client": client,
        "eco_news_id": created_news["id"],
        "news": created_news
    }


@fixture(scope="module")
def created_eco_news_without_image_cleanup(created_eco_news_without_image):
    """Create EcoNews and delete it after all tests in the module."""
    yield created_eco_news_without_image
    client = created_eco_news_without_image["client"]
    eco_news_id = created_eco_news_without_image["eco_news_id"]
    client.delete_eco_news_by_id(eco_news_id)


@fixture(scope="module")
def created_eco_news(auth_token):
    """Create EcoNews with image."""
    client = EcoNewClient(Config.BASE_GREEN_CITY_API_URL, token=auth_token)

    factory = EcoNewsDtoFactory(eco_news_id=0)
    news_dto = factory.create_news_uk()

    response = client.post_eco_news_with_image(
        news_dto,
        str(NewsTestData.TEST_FILE)
    )

    assert_created(response)

    news = response.json()
    eco_news_id = news["id"]

    yield {
        "client": client,
        "eco_news_id": eco_news_id,
        "news": news
    }

    client.delete_eco_news_by_id(eco_news_id)


@fixture(scope="function")
def auth_client_favorite(request):
    """Universal fixture: handles authorization, clears the state for news_id, and performs teardown"""
    auth_api = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_resp = auth_api.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
    token = login_resp.json()["accessToken"]
    # Create a client
    client = EcoNewClient(Config.BASE_GREEN_CITY_API_URL, access_token=token)
    # Getting news_id from class
    news_id = request.param
    client.news_id = news_id
    if news_id:
        with allure.step(f"Pre-test cleanup: Removing news {news_id} from favorites"):
            try:
                client.remove_from_favorites(news_id)
            except Exception as exc:
                allure.attach(
                    str(exc),
                    name=f"Pre-test cleanup failed for news {news_id}",
                )

    yield client

    if news_id:
        with allure.step(f"Post-test cleanup: Removing news {news_id} from favorites"):
            try:
                client.remove_from_favorites(news_id)
            except Exception as exc:
                allure.attach(
                    str(exc),
                    name=f"Post-test cleanup failed for news {news_id}",
                )



@fixture(scope="function")
def comments_client(auth_token):
    client = CommentsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)
    return client


@fixture(scope="session")
def get_auth_token():
    """Get auth token."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    assert login_response.status_code == 200, f"Fixture: Login failed with {login_response.status_code}"

    # Validate response schema to ensure required fields (including accessToken) are present
    validate_json(login_response.json(), success_sign_in_schema)

    token = login_response.json().get("accessToken")
    assert token, "Fixture: Login response does not contain 'accessToken'"
    return token

@fixture(scope="session")
def eco_news_client_with_auth_token(get_auth_token) -> EcoNewsClient:
    return EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, get_auth_token)

@fixture(scope="function")
def create_eco_news(get_auth_token, eco_news_client_with_auth_token) -> tuple[Any, Any]:
    news_payload = {
        "title": "Eco title ",
        "text": "Test content with more than 20 characters",
        "tags": [EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        "source": "https://chatgpt.com/",
        "shortInfo": "short description 12341"
    }
    response = eco_news_client_with_auth_token.add_eco_news(news_payload)
    assert 200 <= response.status_code < 300, (
        f"Fixture: Failed to create eco news, status code {response.status_code}"
    )
    news_response = response.json()
    return get_auth_token, news_response

@fixture(scope="function")
def create_delete_news_with_token(create_eco_news, eco_news_client_with_auth_token):
    with allure.step("Creating news for test and capturing its ID"):
        auth_token, news_response = create_eco_news
        news_id = news_response["id"]

    yield auth_token, news_response

    with allure.step(f"Cleanup: Deleting news ID {news_id}"):
        eco_news_client_with_auth_token.delete_eco_news_by_id(news_id)
