import allure

@allure.feature("Eco News Favorites")
@allure.severity(allure.severity_level.CRITICAL)
class TestFavoriteEcoNews:
    news_id = 100

    @allure.title("Add and remove news from favorites (Authorized)")
    def test_add_remove_favorites_authorized(self, auth_client_favorite):
        # Adding to favorites
        add_resp =auth_client_favorite.add_to_favorites(self.news_id)
        assert add_resp.status_code == 200

        # Removing from favorites
        remove_resp = auth_client_favorite.remove_from_favorites(self.news_id)
        assert remove_resp.status_code == 200

    @allure.title("Add the same news twice - Error 400")
    def test_add_to_favorites_twice_error(self, auth_client_favorite):
        # Perform the first addition to ensure the news is in favorites
        auth_client_favorite.add_to_favorites(self.news_id)

        # Attempting to add the same news item again
        double_add_resp = auth_client_favorite.add_to_favorites(self.news_id)
        assert double_add_resp.status_code == 400

        # Verify the specific error message from the response body
        error_msg = double_add_resp.json().get("message")
        assert error_msg == "User has already added this eco new to favorites."

    @allure.title("Attempt to add to favorites without token - Error 401")
    def test_add_to_favorites_unauthorized(self, auth_client_favorite):

        from clients.eco_new_client import EcoNewClient
        from data.config import Config

        # Create a client without an access token
        unauthorized_client = EcoNewClient(Config.BASE_GREEN_CITY_API_URL)

        resp = unauthorized_client.add_to_favorites(self.news_id)

        # Expecting 401 because no token was provided
        assert resp.status_code == 401