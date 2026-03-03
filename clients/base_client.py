import requests
from requests import Response


class BaseClient:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "accept": "*/*",
            })
        if self.access_token:
            self.session.headers.update({
                "Authorization": "Bearer " + self.access_token,
            })



    def _request(self,method, endpoint, headers=None, **kwargs)->Response:
        url = f"{self.base_url}{endpoint}"

        if headers:
            self.session.headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            **kwargs
        )

        return response