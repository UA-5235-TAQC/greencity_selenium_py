from pytest import fixture
import allure
from clients.eco_new_client import EcoNewClient
from clients.own_security_client import OwnSecurityClient
from data.api_news_test_data import EcoNewsDtoFactory
from data.config import Config
from data.ui_news_test_data import NewsTestData
from models.eco_news_request import EcoNewsRequest
from tests.api.utils.api_test_assertions import assert_ok, assert_created


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
