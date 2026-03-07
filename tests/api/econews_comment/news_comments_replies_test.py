import allure
import pytest
from allure_commons.types import Severity
from clients.eco_news_comment_client import EcoNewsCommentClient
from models.queries import CommentQuery
from tests.api.utils.comment_assertions import assert_comment_response, assert_page_meta


@allure.epic("EcoNewsComment API")
@allure.feature("EcoNews Comments")
@allure.story("Verify replies and replies count for EcoNews comments")
@allure.tag("EcoNewsComment API")
@allure.severity(Severity.NORMAL)
@pytest.mark.usefixtures("create_comments")
class TestEcoNewsCommentReplies:
    """Test suite verifies replies and replies count for EcoNews comments"""

    eco_news_comment_client: EcoNewsCommentClient
    parent_comment_id: int
    parent_sub_comment_id: int
    comment_id_with_images: int
    sub_comment_id_with_images: int
    sub_comment_id: int

    def _verify_active_replies(
            self,
            parent_id: int,
            expected_comment_id: int,
            query: CommentQuery = None,
            reply_index: int = 0
    ):
        """Helper to verify active replies for a given parent comment"""

        response = (
            self.eco_news_comment_client.get_active_replies(parent_id, query)
        )

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        page_response = response.json()

        assert page_response is not None, "Response JSON should not be None"

        page = page_response.get("page")
        assert page is not None, "Page list should not be None"
        assert 0 <= reply_index < len(page), f"Reply index {reply_index} out of range"

        assert_page_meta(
            page_response,
            expected_total_elements=len(page),
            expected_current_page=query.page if query else 0
        )

        active_reply = page[reply_index]

        response = self.eco_news_comment_client.get_comment_by_id(expected_comment_id)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        created_active_reply = response.json()

        assert_comment_response(active_reply, created_active_reply)

        return active_reply

    @allure.description("Verify that active replies for a comment can be retrieved " +
                        "successfully without query parameters.")
    def test_get_active_replies_default(self):
        self._verify_active_replies(
            parent_id=self.comment_id_with_images,
            expected_comment_id=self.sub_comment_id_with_images
        )

    @allure.description(
        "Verify that active replies for a comment can be retrieved "
        "for a specific page (page=0, size=10)."
    )
    def test_get_active_replies_with_page(self):
        self._verify_active_replies(
            parent_id=self.comment_id_with_images,
            expected_comment_id=self.sub_comment_id,
            query=CommentQuery(page=0, size=10),
            reply_index=1
        )

    @allure.description(
        "Verify that active replies for a comment can be retrieved when page size is set to 1."
    )
    def test_get_active_replies_size_one(self):
        self._verify_active_replies(
            parent_id=self.parent_comment_id,
            expected_comment_id=self.parent_sub_comment_id,
            query=CommentQuery(page=0, size=1)
        )
