import allure
from allure_commons.types import Severity
import pytest

from clients.eco_news_client import EcoNewsClient
from data.config import Config


@allure.epic("EcoNews API")
@allure.feature("Eco News Favorites")
@allure.story("Manage favorite news")
@allure.tag("Favorites")
@allure.severity(Severity.CRITICAL)
class TestFavoriteEcoNews:
    """Tests for adding and removing Eco News items from user favorites."""

    @allure.title("Add and remove news from favorites (Authorized)")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_remove_favorites_authorized(self, auth_client_favorite):
        """Test adding a news item to favorites and then removing it."""
        news_id = auth_client_favorite.news_id

        add_resp = auth_client_favorite.add_to_favorites(news_id)
        assert add_resp.status_code == 200

        remove_resp = auth_client_favorite.remove_from_favorites(news_id)
        assert remove_resp.status_code == 200

    @allure.title("Add the same news twice - Error 400")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_to_favorites_twice_error(self, auth_client_favorite, ):
        """Test that adding the same news item to favorites twice results in an error."""
        news_id = auth_client_favorite.news_id
        auth_client_favorite.add_to_favorites(news_id)

        double_add_resp = auth_client_favorite.add_to_favorites(news_id)
        assert double_add_resp.status_code == 400

        error_msg = double_add_resp.json().get("message")
        assert error_msg == "User has already added this eco new to favorites."

    @allure.title("Attempt to add to favorites without token - Error 401")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_to_favorites_unauthorized(self, auth_client_favorite):
        """Test that adding a news item to favorites without authentication returns 401."""
        news_id = auth_client_favorite.news_id
        unauthorized_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL)
        resp = unauthorized_client.add_to_favorites(news_id)
        assert resp.status_code == 401
