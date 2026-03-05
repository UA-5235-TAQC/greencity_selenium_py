import allure
from requests import Response
from clients.base_client import BaseClient


class OwnSecurityClient(BaseClient):
    """ Client for interacting with the OwnSecurity API. """

    def __init__(self, base_url, access_token=None):
        super().__init__(f"{base_url}/ownSecurity", access_token)

    @allure.step("Sign in to the own security service with email: {email}")
    def sign_in(self, email: str, password: str) -> Response:
        """Sign in to the own security service."""
        payload = {
            "email": email,
            "password": password,
            "projectName": "GREENCITY"
        }
        return self.post("/signIn", json=payload)

    @allure.step("Refresh access token using refresh token")
    def refresh_token(self, refresh_token: str) -> Response:
        """Exchange a refresh token for a new access/refresh token pair.

        The GreenCityUser ``/updateAccessToken`` endpoint accepts the refresh
        token as a query parameter and returns a new ``accessToken`` and
        ``refreshToken``.
        """
        return self.post("/updateAccessToken", params={"refreshToken": refresh_token})
