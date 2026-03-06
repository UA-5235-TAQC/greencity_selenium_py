import allure
from jsonschema import validate

from clients.eco_news_client import EcoNewsClient
from data.config import Config
from schemas.greencity.eco_news_tags_schema import eco_news_tags_schema


@allure.feature("Eco News API")
@allure.story("Get eco news tags")
def test_get_tags():
    client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL)

    with allure.step("Send request to get tags"):
        response = client.get_tags("en")

    with allure.step("Verify status code"):
        assert response.status_code == 200

    with allure.step("Verify response schema"):
        tags = response.json()
        validate(instance=tags, schema=eco_news_tags_schema)

    with allure.step("Verify response content"):
        assert len(tags) > 0

        first_tag = tags[0]

        assert isinstance(first_tag["id"], int)
        assert isinstance(first_tag["name"], str)
