import mimetypes

import allure
from dataclasses import asdict
from typing import Optional
import json

from requests import Response
from clients.base_client import BaseClient
from models.eco_news_query import EcoNewsQuery
from models.eco_news_request import EcoNewsRequest
from models.update_eco_news_request import UpdateEcoNewsRequest
from pathlib import Path


class EcoNewClient(BaseClient):
    """Client for interacting with EcoNews API."""

    resource_path = "eco-news"

    def __init__(self, base_url: str, token: Optional[str] = None):
        super().__init__(base_url, token)

    def get_path(self, eco_news_id: int) -> str:
        """Return EcoNews path by ID."""
        return f"{self.resource_path}/{eco_news_id}"

    @allure.step("Get EcoNews with query parameters: {query_params}")
    def get_eco_news(self, query_params: dict) -> Response:
        """Get EcoNews list."""
        return self.get(self.resource_path, params=query_params)

    @allure.step("Post new EcoNews without image")
    def post_eco_news(self, body: EcoNewsRequest) -> Response:
        """Create EcoNews without image."""
        files = {
            "addEcoNewsDtoRequest": (
                "addEcoNewsDtoRequest",
                json.dumps(asdict(body), ensure_ascii=False),
                "application/json"
            )
        }
        headers = {"Content-Type": None}
        return self.post(self.resource_path, files=files, headers=headers)

    @allure.step("Post new EcoNews with image: {image_path}")
    def post_eco_news_with_image(self, body: EcoNewsRequest, image_path: str) -> Response:
        """Create EcoNews with image."""
        dto_json = json.dumps(asdict(body), ensure_ascii=False)
        files = {
            "addEcoNewsDtoRequest": ("addEcoNewsDtoRequest", dto_json, "application/json")
        }
        headers = {"Content-Type": None}

        image_path = Path(image_path)
        mime_type, _ = mimetypes.guess_type(image_path)
        mime_type = mime_type or "application/octet-stream"

        with open(image_path, "rb") as img_file:
            files["image"] = (image_path.name, img_file, mime_type)
            return self.post(self.resource_path, files=files, headers=headers)

    @allure.step("Get EcoNews by ID: {eco_news_id}")
    def get_eco_news_by_id(self, eco_news_id: int) -> Response:
        """Get EcoNews by ID."""
        return self.get(self.get_path(eco_news_id))

    @allure.step("Delete EcoNews by ID: {eco_news_id}")
    def delete_eco_news_by_id(self, eco_news_id: int) -> Response:
        """Delete EcoNews by ID."""
        return self.delete(self.get_path(eco_news_id))

    @allure.step("Get EcoNews count by author id: {author_id}")
    def get_eco_news_count_by_author_id(self, author_id: int) -> Response:
        """Get EcoNews count by author."""
        return self.get(f"{self.resource_path}/count", params={"author-id": author_id})

    @allure.step("Get EcoNews with typed query parameters: {query}")
    def get_eco_news_by_query(self, query: EcoNewsQuery) -> Response:
        """Get EcoNews using EcoNewsQuery object."""
        params = {}
        if query.author_id is not None:
            params["author-id"] = query.author_id
        if query.favorite is not None:
            params["favorite"] = query.favorite
        if query.page is not None:
            params["page"] = query.page
        if query.size is not None:
            params["size"] = query.size
        return self.get(self.resource_path, params=params)

    @allure.step("Get tags with language: {lang}")
    def get_tags(self, lang: str) -> Response:
        """Get EcoNews tags."""
        return self.get(f"{self.resource_path}/tags", params={"lang": lang})

    @allure.step("Add EcoNews to favorites: {eco_news_id}")
    def add_to_favorites(self, eco_news_id: int) -> Response:
        """Add EcoNews to favorites."""
        return self.post(f"{self.get_path(eco_news_id)}/favorites")

    @allure.step("Remove EcoNews from favorites: {eco_news_id}")
    def remove_from_favorites(self, eco_news_id: int) -> Response:
        """Remove EcoNews from favorites."""
        return self.delete(f"{self.get_path(eco_news_id)}/favorites")

    @allure.step("Like EcoNews by ID: {eco_news_id}")
    def like_eco_news_by_id(self, eco_news_id: int) -> Response:
        """Toggle like."""
        return self.post(f"{self.get_path(eco_news_id)}/likes")

    @allure.step("Count likes on EcoNews: {eco_news_id}")
    def count_eco_news_likes(self, eco_news_id: int) -> Response:
        """Get like count."""
        return self.get(f"{self.get_path(eco_news_id)}/likes/count")


    @allure.step("Update EcoNews by ID: {eco_news_id}")
    def update_eco_news_by_id(self, eco_news_id: int, update_dto: UpdateEcoNewsRequest,
                              image_path: Optional[str] = None) -> Response:
        """Update EcoNews with optional image."""
        dto_dict = asdict(update_dto)
        dto_dict["shortInfo"] = dto_dict.pop("short_info")
        dto_json = json.dumps(dto_dict, ensure_ascii=False)
        files = {
            "updateEcoNewsDto": ("updateEcoNewsDto", dto_json, "application/json")
        }
        headers = {"Content-Type": None}

        if image_path:
            image_path = Path(image_path)
            mime_type, _ = mimetypes.guess_type(image_path)
            mime_type = mime_type or "application/octet-stream"

            with open(image_path, "rb") as img_file:
                files["image"] = (image_path.name, img_file, mime_type)
                return self.put(self.get_path(eco_news_id), files=files, headers=headers)

        return self.put(self.get_path(eco_news_id), files=files, headers=headers)

    @allure.step("Get EcoNews by ID with language: {lang}")
    def get_eco_news_by_id_with_lang(self, eco_news_id: int, lang: str) -> Response:
        """Get EcoNews by ID with language."""
        return self.get(self.get_path(eco_news_id), params={"lang": lang})

    @allure.step("Add news {news_id} to favorites")
    def add_to_favorites(self, news_id: int) -> Response:
        """Endpoint: POST .../eco-news/{id}/favorites"""
        return self.post(f"{news_id}/favorites")

    @allure.step("Remove news {news_id} from favorites")
    def remove_from_favorites(self, news_id: int) -> Response:
        """Endpoint: DELETE .../eco-news/{id}/favorites"""
        return self.delete(f"{news_id}/favorites")
