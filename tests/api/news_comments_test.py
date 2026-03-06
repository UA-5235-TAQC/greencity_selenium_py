import allure
import pytest
from allure_commons.types import Severity
from data.config import Config
from data.ui_news_test_data import NewsTestData
from schemas.greencity.get_comment_by_id_response_schema import get_comment_by_id_response_schema
from schemas.greencity.comment_creation_schema import comment_creation_schema
from tests.utils.validators import validate_json
from clients.eco_news_comment_client import EcoNewsCommentClient

class TestNewsComments:

    @allure.severity(Severity.NORMAL)
    @pytest.mark.dependency(name="add_comment_to_eco_news")
    def test_add_comment_to_eco_news(self, create_delete_news_with_token):
        """Test: Add a comment to eco news."""
        access_token, news_response = create_delete_news_with_token
        news_id = news_response["id"]
        comment_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token, news_id)
        response = comment_client.add_comment("This is a test comment.", NewsTestData.TEST2_FILE)
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        is_valid, error = validate_json(response.json(), comment_creation_schema)
        assert is_valid, f"Response JSON does not match the expected schema: {error}"

    @allure.severity(Severity.NORMAL)
    def test_like_comment(self, create_and_cleanup_comment):
        """Test: Like a comment."""
        access_token, _ = create_and_cleanup_comment
        comment_id = 2864  #TODO Replace with a dynamic comment ID. Need a second test account.
        comment_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token)
        response = comment_client.like_comment(comment_id)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


    @allure.severity(Severity.TRIVIAL)
    def test_get_comment_by_id(self, create_and_cleanup_comment):
        """Test: Get a comment by its ID."""
        access_token, comment_response = create_and_cleanup_comment
        comment_id = comment_response["id"]
        comment_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token)
        response = comment_client.get_comment_by_id(comment_id)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        is_valid, error = validate_json(response.json(), get_comment_by_id_response_schema)
        assert is_valid, f"Response JSON does not match the expected schema: {error}"

    @allure.severity(Severity.TRIVIAL)
    def test_delete_comment_by_id(self, create_comment_with_token):
        """Test: Delete a comment by its ID."""
        access_token, _, comment_response = create_comment_with_token
        comment_id = comment_response["id"]
        comment_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token)
        response = comment_client.delete_comment_by_id(comment_id)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
       