import allure
import pytest

from clients.eco_news_client import EcoNewsClient
from data.config import Config


@allure.feature("Eco News Favorites")
@allure.severity(allure.severity_level.CRITICAL)
class TestFavoriteEcoNews:

    @allure.title("Add and remove news from favorites (Authorized)")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_remove_favorites_authorized(self, auth_client_favorite):
        news_id = auth_client_favorite.news_id

        # Adding to favorites

        add_resp = auth_client_favorite.add_to_favorites(news_id)
        assert add_resp.status_code == 200

        # Removing from favorites
        remove_resp = auth_client_favorite.remove_from_favorites(news_id)
        assert remove_resp.status_code == 200

    @allure.title("Add the same news twice - Error 400")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_to_favorites_twice_error(self, auth_client_favorite, ):
        # Perform the first addition to ensure the news is in favorites
        news_id = auth_client_favorite.news_id
        auth_client_favorite.add_to_favorites(news_id)

        # Attempting to add the same news item again
        double_add_resp = auth_client_favorite.add_to_favorites(news_id)
        assert double_add_resp.status_code == 400

        # Verify the specific error message from the response body
        error_msg = double_add_resp.json().get("message")
        assert error_msg == "User has already added this eco new to favorites."

    @allure.title("Attempt to add to favorites without token - Error 401")
    @pytest.mark.parametrize("auth_client_favorite", [Config.FAVORITE_NEWS_ID], indirect=True)
    def test_add_to_favorites_unauthorized(self, auth_client_favorite):
        news_id = auth_client_favorite.news_id
        # Create a client without an access token
        unauthorized_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL)

        resp = unauthorized_client.add_to_favorites(news_id)

        # Expecting 401 because no token was provided
        assert resp.status_code == 401
