import pytest
import allure
from allure_commons.types import Severity

from clients.eco_new_client import EcoNewClient
from data.api_news_test_data import EcoNewsDtoFactory
from models.update_eco_news_request import UpdateEcoNewsRequest
from tests.api.utils.api_test_assertions import assert_unauthorized, assert_ok
from tests.api.utils.econews_assertions import assert_eco_news_json


@allure.epic("EcoNews API")
@allure.feature("EcoNews CRUD without authorization")
@allure.tag("EcoNewsById API")
@allure.severity(Severity.NORMAL)
class TestUnauthorizedEcoNewsById:
    """Tests for EcoNews API endpoints without authorization."""

    @allure.story("Update EcoNews without token")
    @allure.description("Verify that updating EcoNews without authorization returns 401 status code.")
    def test_update_eco_news_by_id_without_token(self, eco_news_setup):
        """ Test updating an EcoNews item without providing an authorization token. """
        client = eco_news_setup["client"]
        eco_news_id = eco_news_setup["eco_news_id"]
        update_dto = UpdateEcoNewsRequest(
            id=eco_news_id,
            title="Another string",
            content="Test content with more than 20 chars",
            short_info="Short info",
            tags=[]
        )
        response = client.update_eco_news_by_id(eco_news_id, update_dto)
        assert_unauthorized(response)

    @allure.story("Delete EcoNews without token")
    @allure.description("Verify that deleting EcoNews without authorization returns 401 status code.")
    def test_delete_eco_news_by_id_without_token(self, eco_news_setup):
        """ Test deleting an EcoNews item without providing an authorization token. """
        client = eco_news_setup["client"]
        eco_news_id = eco_news_setup["eco_news_id"]
        response = client.delete_eco_news_by_id(eco_news_id)
        assert_unauthorized(response)


@pytest.mark.epic("EcoNews API")
@pytest.mark.feature("Update EcoNews without image")
@pytest.mark.tag("EcoNewsById API")
@pytest.mark.severity(Severity.NORMAL)
class TestEcoNewsById:

    @allure.story("Update EcoNews without image")
    @allure.description("Verify that updating EcoNews without providing an image works correctly")
    def test_update_eco_news_by_id_without_image(self, created_eco_news):
        """ Test for updating EcoNews without providing an image. """
        client: EcoNewClient = created_eco_news["client"]
        eco_news_id: int = created_eco_news["eco_news_id"]
        dto_factory = EcoNewsDtoFactory(eco_news_id)
        update_dto: UpdateEcoNewsRequest = dto_factory.update_dto_uk()
        response = client.update_eco_news_by_id(eco_news_id, update_dto)
        assert_ok(response)
        response_json = response.json()
        assert_eco_news_json(response_json)

        assert response_json["title"] == update_dto.title
        assert response_json["content"] == update_dto.content
        assert response_json["shortInfo"] == update_dto.short_info
        assert response_json["source"] == update_dto.source
        assert response_json.get("hidden", False) is False
        assert response_json.get("likes", 0) == 0
        assert response_json.get("dislikes", 0) == 0
        assert response_json.get("countComments", 0) == 0
