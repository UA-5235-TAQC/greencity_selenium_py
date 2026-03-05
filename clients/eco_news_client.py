import json
import mimetypes
import os

import allure

from clients.base_client import BaseClient


class EcoNewsClient(BaseClient):
    def __init__(self, base_url, access_token=None):
        super().__init__(f"{base_url}/eco-news", access_token)


    @allure.step("Create new Eco News with image: {image_path}")
    def add_eco_news(self, news_data: dict, image_path: str = None):
        endpoint = ""

        if image_path:
            file_name = os.path.basename(image_path)
            mime_type,  = mimetypes.guess_type(image_path)

            with open(image_path, 'rb') as image_file:
                files = {
                    'addEcoNewsDtoRequest': (None, json.dumps(news_data), 'application/json'),
                    'image': (file_name, image_file, mime_type),
                }

                return self._request(
                    "POST",
                    endpoint,
                    headers={"Content-Type": None},
                    files=files
                )
        else:
            files = {
                'addEcoNewsDtoRequest': (None, json.dumps(news_data), 'application/json')
            }

            return self.post(
                endpoint,
                headers={"Content-Type": None},
                files=files
            )
    

    @allure.step("Delete Eco News by id: {news_id}")
    def delete_eco_news_by_id(self, news_id: int):
        return self.delete(f"/{news_id}")