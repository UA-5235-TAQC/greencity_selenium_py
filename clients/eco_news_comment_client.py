import json

import allure

from clients.base_client import BaseClient


class EcoNewsCommentClient(BaseClient):
    def __init__(self, base_url, access_token=None, news_id: int = None):
        super().__init__(f"{base_url}/eco-news", access_token)
        self.news_id = news_id

    @allure.step("Add a comment to eco news with Id")
    def add_comment(self, text: str, image_path: str = None):
        """Adds a comment. If image_path is specified, it adds it with the photo, if not, it adds it without."""
        if self.news_id is None:
            raise ValueError("news_id must be set on EcoNewsCommentClient before adding a comment.")

        endpoint = f"/{self.news_id}/comments"

        request_data = {"text": text, "parentCommentId": 0}

        multi_files = [('request', (None, json.dumps(request_data), 'application/json'))]

        if image_path:
            self.attach_images_to_multipart(multi_files, "images", [image_path])

        return self.post(endpoint, files=multi_files, headers={"Content-Type": None})

    @allure.step("Like comment")
    def like_comment(self, comment_id: int):
        return self.post("/comments/like", params={"commentId": comment_id})

    @allure.step("Getting comment by Id")
    def get_comment_by_id(self, comment_id: int):
        return self.get(f"/comments/{comment_id}")

    @allure.step("Deleting comment by Id")
    def delete_comment_by_id(self, comment_id: int):
        return self.delete(f"/comments/{comment_id}")
