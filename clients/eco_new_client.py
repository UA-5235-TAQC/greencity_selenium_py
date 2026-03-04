import json
import mimetypes
import os

import allure
from requests import Response

from clients.base_client import BaseClient


class EcoNewsClient(BaseClient):
    """Client for interacting with the Eco News API,
     extending BaseClient for common functionality."""

    def __init__(self, base_url, access_token=None):
        super().__init__(base_url=f"{base_url}/eco-news", access_token=access_token)

    @allure.step("Find eco news by page with filters: tags={tags}, title={title}, "
                 "author_id={author_id}, favorite={favorite}, page={page}, size={size}, "
                 "sort={sort}")
    def find_eco_news_by_page(self,
                              tags: list[str] = None,
                              title: str = None,
                              author_id: int = None,
                              favorite: bool = False,
                              page: int = 0,
                              size: int = 20,
                              sort: list[str] = None) -> Response:
        params = {
            "page": page,
            "size": size,
            "favorite": str(favorite).lower()
        }

        optional_params = {
            "tags": ",".join(tags) if tags else None,
            "title": title,
            "authorId": author_id,
            "sort": sort
        }

        params.update({k: v for k, v in optional_params.items() if v is not None})

        return self._request("GET", "", params=params)

    @allure.step("Create new Eco News with image: {image_path}")
    def add_eco_news(self, news_data: dict, image_path: str = None):
        endpoint = ""

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
