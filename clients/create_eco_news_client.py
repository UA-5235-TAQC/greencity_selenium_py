import json
import mimetypes
import os

import allure

from clients.base_client import BaseClient


class EcoNewsClient(BaseClient):
    def __init__(self, base_url, access_token=None):
        super().__init__(f"{base_url}", access_token)


    @allure.step("Create new Eco News with image: {image_path}")
    def add_eco_news(self, news_data: dict, image_path: str = None):
        endpoint = "/eco-news"

        files = {
            'addEcoNewsDtoRequest': (None, json.dumps(news_data), 'application/json')
        }

        if image_path:
            file_name = os.path.basename(image_path)

            mime_type, _ = mimetypes.guess_type(image_path)
            files['image'] = (file_name, open(image_path, 'rb'), mime_type)

        return self._request(
            "POST",
            endpoint,
            headers={"Content-Type": None},
            files=files
        )
