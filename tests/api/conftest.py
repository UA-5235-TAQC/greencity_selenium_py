from pytest import fixture
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
