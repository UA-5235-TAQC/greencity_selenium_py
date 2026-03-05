import json
import allure
from requests import Response
from clients.base_client import BaseClient


class CommentsClient(BaseClient):

    def __init__(self, base_url, access_token=None):
        """Client for interacting with the News Comments API,
        extending BaseClient for common functionality."""
        super().__init__(base_url=f"{base_url}/eco-news", access_token=access_token)

    @allure.step("Add comment")
    def get_comments_count(self, news_id: int) -> Response:
        """Get comments count for a particular news"""
        endpoint = f"/{news_id}/comments/count"
        return self._request(method="GET", endpoint=endpoint)

    @allure.step("Dislike comment and get comment instance")
    def dislike_comment_and_get_instance(self, comment_id: int) -> Response:
        """Dislike comment and get instance"""
        endpoint = "/comments/dislikeV2"
        return self._request(method="POST", endpoint=endpoint, params={"commentId": comment_id})

    @allure.step("like comment and get comment instance")
    def like_comment_and_get_instance(self, comment_id: int) -> Response:
        """Like comment and get instance"""
        endpoint = "/comments/likeV2"
        return self._request(method="POST", endpoint=endpoint, params={"commentId": comment_id})

    @allure.step("delete comment")
    def delete_comment(self, comment_id: int) -> Response:
        """Delete comment"""
        endpoint = f"/comments/{comment_id}"
        return self._request(method="DELETE", endpoint=endpoint)

    @allure.step("Get comment by ID")
    def get_comment_by_id(self, comment_id: int) -> Response:
        """Get comment by id"""
        endpoint = f"/comments/{comment_id}"
        return self._request(method="GET", endpoint=endpoint)

    @allure.step("Like or unlike comment")
    def like_comment(self, comment_id: int) -> Response:
        """Like / Unlike comment"""
        endpoint = "/comments/like"
        return self._request(method="POST", endpoint=endpoint, params={"commentId": comment_id})

    @allure.step("Dislike comment or remove dislike")
    def dislike_comment(self, comment_id: int) -> Response:
        """Dislike / Remove Dislike comment"""
        endpoint = "/comments/dislike"
        return self._request(method="POST", endpoint=endpoint, params={"commentId": comment_id})

    @allure.step("Get all comments")
    def get_all_active_comments(self, news_id: int, page_index: int, size: int) -> Response:
        """Get all active comments"""
        endpoint = f"/{news_id}/comments/active"
        return self._request(method="GET", endpoint=endpoint, params={"page": page_index, "size": size})

    @allure.step("Get all active comment replies")
    def get_all_comment_replies(self, parent_comment_id: int, page_index: int, size: int) -> Response:
        """Get all active comment replies"""
        endpoint = f"/comments/{parent_comment_id}/replies/active"
        return self._request(method="GET", endpoint=endpoint, params={"page": page_index, "size": size})

    @allure.step("Get comment replies count")
    def get_comment_replies_count(self, parent_comment_id: int) -> Response:
        """Get comment replies count"""
        endpoint = f"/comments/{parent_comment_id}/replies/active/count"
        return self._request(method="GET", endpoint=endpoint)

    @allure.step("Update comment")
    def update_comment(self, comment_id: int, text: str) -> Response:
        """Update comment"""
        endpoint = "/comments"
        return self._request(method="PATCH",
                             endpoint=endpoint,
                             params={"commentId": comment_id},
                             json=text)

    @allure.step("Add comment")
    def add_comment(self, news_id: int,
                    comment_message: str,
                    image_url=None,
                    parent_id: int=0,
                    select_default_image: bool=False) -> Response:

        """Add comment to news or reply another comment"""

        endpoint = f"/{news_id}/comments"
        base_image_url = "./data/images/test2.png"
        headers = {"Content-Type": None}
        img_url = image_url if image_url else base_image_url
        file_name = os.path.basename(image_url or base_image_url)

        with open(img_url, "rb") as img:
            files = {
                "request": (json.dumps({
                    "text": comment_message,
                    "parentCommentId": parent_id
                })),
                "images": None if not select_default_image else [file_name, img, "image/jpeg"]
            }

            return self._request(method="POST",
                                 endpoint=endpoint,
                                 files=files,
                                 headers=headers)