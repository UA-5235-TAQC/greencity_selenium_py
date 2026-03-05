import pytest
import allure
from allure_commons.types import Severity

from clients.eco_news_comment_client import EcoNewsCommentClient
from models.queries import CommentQuery
from tests.api.utils.comment_assertions import assert_comment_response, assert_page_meta


@allure.epic("EcoNewsComment API")
@allure.feature("EcoNews Comments")
@allure.story("Verify replies and replies count for EcoNews comments")
@allure.tag("EcoNewsComment API")
@pytest.mark.severity(Severity.NORMAL)
@pytest.mark.usefixtures("create_comments")
class TestEcoNewsCommentReplies:
    """Test suite verifies replies and replies count for EcoNews comments"""

    eco_news_comment_client: EcoNewsCommentClient
    comment_id_with_images: int
    sub_comment_id_with_images: int

    @allure.description("Verify that active replies for a comment can be retrieved " +
            "successfully without query parameters.")
    def test_get_active_replies_default(self):
        page_response = self.eco_news_comment_client.get_active_replies_default(
            self.comment_id_with_images)
        assert page_response is not None, "Response should not be None"

        assert_page_meta(page_response, expected_total_elements=2, expected_current_page=0)
        first_active_reply = page_response.get("page")[0]
        response = self.eco_news_comment_client.get_comment_by_id(
            self.sub_comment_id_with_images)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        created_active_reply = response.json()

        assert_comment_response(first_active_reply, created_active_reply)

