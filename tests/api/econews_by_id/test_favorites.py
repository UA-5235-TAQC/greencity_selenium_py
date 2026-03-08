import allure
from allure_commons.types import Severity
import pytest

from clients.eco_news_client import EcoNewsClient
from data.config import Config
from tests.api.utils.api_test_assertions import assert_ok, assert_bad_request, assert_unauthorized


@allure.epic("EcoNews API")
@allure.feature("Eco News Favorites")
@allure.story("Manage favorite news")
@allure.tag("Favorites")
@allure.severity(Severity.CRITICAL)
class TestFavoriteEcoNews:
    """Tests for adding and removing Eco News items from user favorites."""

    @allure.title("Add and remove news from favorites (Authorized)")
    def test_add_remove_favorites_authorized(self, auth_client_favorite):
        """Test adding a news item to favorites and then removing it."""
        client = auth_client_favorite["client"]
        news_id = auth_client_favorite["news_id"]

        add_resp = client.add_to_favorites(news_id)
        assert_ok(add_resp)

        remove_resp = client.remove_from_favorites(news_id)
        assert_ok(remove_resp)

    @allure.title("Add the same news twice - Error 400")
    def test_add_to_favorites_twice_error(self, auth_client_favorite):
        """Test that adding the same news item to favorites twice results in an error."""
        client = auth_client_favorite["client"]
        news_id = auth_client_favorite["news_id"]

        client.add_to_favorites(news_id)

        double_add_resp = client.add_to_favorites(news_id)
        assert_bad_request(
            double_add_resp,
            "User has already added this eco new to favorites."
        )

    @allure.title("Attempt to add to favorites without token - Error 401")
    def test_add_to_favorites_unauthorized(self, auth_client_favorite):
        """Test that adding a news item to favorites without authentication returns 401."""
        news_id = auth_client_favorite["news_id"]

        unauthorized_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL)
        resp = unauthorized_client.add_to_favorites(news_id)

        assert_unauthorized(resp)
