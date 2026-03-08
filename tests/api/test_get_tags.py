import allure
from allure_commons.types import Severity
from jsonschema import validate

from clients.eco_news_client import EcoNewsClient
from data.config import Config
from schemas.greencity.eco_news_tags_schema import eco_news_tags_schema
from tests.api.utils.api_test_assertions import assert_ok


@allure.epic("EcoNews API")
@allure.feature("EcoNews tags")
@allure.story("Retrieve available EcoNews tags")
@allure.title("Get EcoNews tags by language")
@allure.tag("EcoNews API")
@allure.severity(Severity.NORMAL)
def test_get_tags():
    """Verify that the EcoNews API returns a list of available tags."""
    client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL)

    with allure.step("Send request to get tags"):
        response = client.get_tags("en")

    with allure.step("Verify status code"):
        assert_ok(response)

    with allure.step("Verify response schema"):
        tags = response.json()
        validate(instance=tags, schema=eco_news_tags_schema)

    with allure.step("Verify response content"):
        assert len(tags) > 0

        first_tag = tags[0]

        assert isinstance(first_tag["id"], int)
        assert isinstance(first_tag["name"], str)
