import allure

from clients.base_client import BaseClient


class OwnSecurityClient(BaseClient):
    def __init__(self, base_url, access_token=None):
        super().__init__(f"{base_url}/ownSecurity", access_token)

    @allure.step("Sign in to the own security service with email: {email}")
    def sign_in(self, email: str, password: str):
        """Sign in to the own security service."""
        endpoint = "/signIn"
        payload = {
            "email": email,
            "password": password,
            "projectName": "GREENCITY"
        }
        return self._request("POST", endpoint, json=payload)