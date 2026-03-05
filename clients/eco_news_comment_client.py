import allure

from clients.base_client import BaseClient
import json
import mimetypes
from pathlib import Path

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
    
        request_data = {
            "text": text,
            "parentCommentId": 0
        }

        headers = {"Content-Type": None}

        if image_path:
            file_name = Path(image_path).name

            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = 'application/octet-stream'

            with open(image_path, 'rb') as image_file:
                files = {
                    'request': (None, json.dumps(request_data), 'application/json'),
                    'images': (file_name, image_file, mime_type),
                }
                return self._request("POST", endpoint, files=files, headers=headers)
        else:
            files = {
                'request': (None, json.dumps(request_data), 'application/json')
            }
            return self._request("POST", endpoint, files=files, headers=headers)
    
        
    

    @allure.step("Like comment")
    def like_comment(self, comment_id: int):
        """Likes a comment. The parameter is passed as a Query string."""
        endpoint = "/comments/like"
        params = { "commentId": comment_id }
        return self._request("POST", endpoint, params=params)
    

    @allure.step("Getting comment by Id")
    def get_comment_by_id(self, comment_id: int):
        """Gets a comment by its ID."""
        endpoint = f"/comments/{comment_id}"
        return self._request("GET", endpoint)
    
    @allure.step("Deleting comment by Id")
    def delete_comment_by_id(self, comment_id: int):
        """Deletes a comment by its ID."""
        endpoint = f"/comments/{comment_id}"
        return self._request("DELETE", endpoint)
        