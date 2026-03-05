"""Client for interacting with the Eco News API, extending BaseClient for common functionality."""
import allure
from requests import Response
from clients.base_client import BaseClient


class EcoNewClient(BaseClient):
    """Client for interacting with the Eco News API,
     extending BaseClient for common functionality."""
    def __init__(self, base_url, access_token=None):
        """Client for interacting with the Eco News API,
        extending BaseClient for common functionality."""
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
        """Find eco news by page with optional filters and sorting."""
        params = {
            "favorite": favorite,
            "page": page,
            "size": size,
        }

        # ToDo: Refactor to use a more flexible approach for handling filters and sorting
        if tags:
            params["tags"] = ",".join(tags)
        if title:
            params["title"] = title
        if author_id:
            params["authorId"] = author_id
        if sort:
            params["sort"] = ",".join(sort)

        return self._request("GET", "", params=params)

    @allure.step("Add news {news_id} to favorites")
    def add_to_favorites(self, news_id: int) -> Response:
        """Endpoint: POST .../eco-news/{id}/favorites"""
        return self._request("POST", f"/{news_id}/favorites")

    @allure.step("Remove news {news_id} from favorites")
    def remove_from_favorites(self, news_id: int) -> Response:
        """Endpoint: DELETE .../eco-news/{id}/favorites"""
        return self._request("DELETE", f"/{news_id}/favorites")

