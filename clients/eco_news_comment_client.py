from typing import Optional, Dict, List
from requests import Response
import allure

from clients.base_client import BaseClient
import json
import mimetypes
from pathlib import Path

from models.queries import CommentQuery


class EcoNewsCommentClient(BaseClient):
    """Client for interacting with EcoNews comments API."""

    def __init__(self, base_url: str, access_token: str = None, news_id: int = None):
        """Initialize the EcoNewsCommentClient."""
        super().__init__(f"{base_url}/eco-news", access_token)
        self.news_id = news_id

    @allure.step("Add a comment to eco news with Id")
    def add_comment(self, text: str, parent_comment_id: int = 0, image_paths: Optional[List[str]] = None):
        """Add a comment with multiple images."""
        if self.news_id is None:
            raise ValueError("news_id must be set")

        endpoint = f"/{self.news_id}/comments"
        request_data = {"text": text, "parentCommentId": parent_comment_id}

        files: List = [
            ('request', (None, json.dumps(request_data), 'application/json'))
        ]

        if image_paths:
            for image_path in image_paths:
                file_name = Path(image_path).name
                mime_type, _ = mimetypes.guess_type(image_path)
                mime_type = mime_type or 'application/octet-stream'
                files.append(('images', (file_name, open(image_path, 'rb'), mime_type)))

        return self.post(endpoint, files=files, headers={"Content-Type": None})

    @allure.step("Like comment")
    def like_comment(self, comment_id: int):
        """Likes a comment. The parameter is passed as a Query string."""
        endpoint = "/comments/like"
        params = {"commentId": comment_id}
        return self.post(endpoint, params=params)

    @allure.step("Getting comment by Id")
    def get_comment_by_id(self, comment_id: int):
        """Gets a comment by its ID."""
        endpoint = f"/comments/{comment_id}"
        return self.get(endpoint)

    @allure.step("Deleting comment by Id")
    def delete_comment_by_id(self, comment_id: int):
        """Deletes a comment by its ID."""
        endpoint = f"/comments/{comment_id}"
        return self.delete(endpoint)

    @allure.step("API: Get all active replies for comment ID {parent_comment_id} with query params")
    def get_active_replies(self, parent_comment_id: int, query: Optional[CommentQuery] = None) -> Dict:
        """Get all active replies for a comment, optionally with pagination and sorting."""
        params = {}
        if query:
            if query.page is not None:
                params["page"] = query.page
            if query.size is not None:
                params["size"] = query.size
            if query.sort:
                params["sort"] = query.sort
        endpoint = f"/comments/{parent_comment_id}/replies/active"
        response = self.get(endpoint, params=params)
        return response.json()

    @allure.step("API: Get all active replies for comment ID {parent_comment_id} with default pagination")
    def get_active_replies_default(self, parent_comment_id: int) -> Dict:
        """Get all active replies for a comment using default pagination."""
        default_query = CommentQuery(page=0, size=20)
        return self.get_active_replies(parent_comment_id, query=default_query)

    @allure.step("Delete comment with children by ID {comment_id}")
    def delete_comment_with_children(self, comment_id: int):
        """Recursively deletes a comment and all its active replies."""
        replies = self.get_active_replies(comment_id).get("page", [])
        for reply in replies:
            self.delete_comment_with_children(reply["id"])
        return self.delete_comment_by_id(comment_id)

    @allure.step("Count active replies for comment ID {parent_comment_id}")
    def count_active_replies(self, parent_comment_id: int) -> int:
        """Return the count of active replies for a comment."""
        endpoint = f"/comments/{parent_comment_id}/replies/active/count"
        response = self.get(endpoint)
        return response.json().get("count", 0)

    @allure.step("Get comments count")
    def get_comments_count(self, news_id: int) -> Response:
        """Get comments count for a particular news"""
        endpoint = f"/{news_id}/comments/count"
        return self.get(endpoint)

    @allure.step("Dislike comment and get comment instance")
    def dislike_comment_and_get_instance(self, comment_id: int) -> Response:
        """Dislike comment and get instance"""
        endpoint = "/comments/dislikeV2"
        return self.post(path=endpoint, params={"commentId": comment_id})

    @allure.step("like comment and get comment instance")
    def like_comment_and_get_instance(self, comment_id: int) -> Response:
        """Like comment and get instance"""
        endpoint = "/comments/likeV2"
        return self.post(path=endpoint, params={"commentId": comment_id})

    @allure.step("Dislike comment or remove dislike")
    def dislike_comment(self, comment_id: int) -> Response:
        """Dislike / Remove Dislike comment"""
        endpoint = "/comments/dislike"
        return self.post(endpoint, params={"commentId": comment_id})

    @allure.step("Get all comments")
    def get_all_active_comments(self, news_id: int, page_index: int, size: int) -> Response:
        """Get all active comments"""
        endpoint = f"/{news_id}/comments/active"
        return self.get(endpoint, params={"page": page_index, "size": size})

    @allure.step("Update comment")
    def update_comment(self, comment_id: int, text: str) -> Response:
        """Update comment"""
        endpoint = "/comments"
        return self.patch(endpoint, params={"commentId": comment_id}, json_patch=text)
