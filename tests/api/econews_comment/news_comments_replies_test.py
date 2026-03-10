from dateutil.parser import parse

import allure
import pytest
from allure_commons.types import Severity
from clients.eco_news_comment_client import EcoNewsCommentClient
from data.comment_factory import another_sub_comment
from models.queries import CommentQuery
from tests.utils.api_test_assertions import assert_created
from tests.utils.comment_assertions import assert_comment_response, assert_page_meta


@allure.epic("EcoNewsComment API")
@allure.feature("EcoNews Comments")
@allure.story("Verify replies and replies count for EcoNews comments")
@allure.tag("EcoNewsComment API")
@allure.severity(Severity.NORMAL)
@pytest.mark.usefixtures("create_comments")
class TestEcoNewsCommentReplies:
    """Test suite verifies replies and replies count for EcoNews comments"""

    eco_news_comment_client: EcoNewsCommentClient
    comment_ids: dict

    def _verify_active_replies(
            self,
            parent_id: int,
            expected_comment_id: int,
            query: CommentQuery = None,
            reply_index: int = 0
    ):
        """Helper to verify active replies for a given parent comment"""

        response = self.eco_news_comment_client.get_active_replies(parent_id, query)

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

    @allure.title(
        "Verify that active replies for a comment can be retrieved successfully without query parameters."
    )
    def test_get_active_replies_default(self):
        self._verify_active_replies(
            parent_id=self.comment_ids["with_images"],
            expected_comment_id=self.comment_ids["sub_with_images"]
        )

    @allure.title(
        "Verify that active replies for a comment can be retrieved for a specific page (page=0, size=10)."
    )
    def test_get_active_replies_with_page(self):
        self._verify_active_replies(
            parent_id=self.comment_ids["with_images"],
            expected_comment_id=self.comment_ids["sub"],
            query=CommentQuery(page=0, size=10),
            reply_index=1
        )

    @allure.title(
        "Verify that active replies for a comment can be retrieved when page size is set to 1."
    )
    def test_get_active_replies_size_one(self):
        self._verify_active_replies(
            parent_id=self.comment_ids["parent"],
            expected_comment_id=self.comment_ids["parent_sub"],
            query=CommentQuery(page=0, size=1)
        )

    def _create_comment_and_get_id(self, parent_id: int, text: str) -> int:
        """Helper to create a sub-comment and return its ID."""
        response = self.eco_news_comment_client.add_comment(text=text, parent_comment_id=parent_id)
        assert_created(response)
        return response.json()["id"]

    def assert_sorted_by_date(self, replies: list[dict], field_name: str, descending: bool = True):
        """Checks that the list of comments is sorted by date."""
        for i in range(len(replies) - 1):
            current = parse(replies[i][field_name])
            next_ = parse(replies[i + 1][field_name])
            if descending:
                assert current >= next_, f"Replies should be sorted descending by {field_name}"
            else:
                assert current <= next_, f"Replies should be sorted ascending by {field_name}"

    @allure.title("Verify active replies are correctly sorted by createdDate and modifiedDate")
    def test_sort_by_dates(self):
        """
        Verify that active replies are correctly sorted:
        1. By createdDate in descending order
        2. By modifiedDate in descending order
        3. By multiple fields (createdDate, modifiedDate) in descending order
        """
        comment_id_with_images = self.comment_ids["with_images"]
        sub_comment_id = self.comment_ids["sub"]
        sub_comment_id_with_images = self.comment_ids["sub_with_images"]

        with allure.step("Create another sub-comment for sorting test"):
            response = self.eco_news_comment_client.add_comment(
                text=another_sub_comment(),
                parent_comment_id=comment_id_with_images
            )
            assert_created(response)
            another_sub_comment_id = response.json()["id"]

        with allure.step("Verify replies sorted by createdDate descending"):
            sort_params = ["createdDate,desc"]
            query = CommentQuery(page=0, size=20, sort=sort_params)
            page_response = self.eco_news_comment_client.get_active_replies(
                parent_comment_id=comment_id_with_images,
                query=query
            ).json()

            replies = page_response["page"]

            self.assert_sorted_by_date(replies, "createdDate", descending=True)
            assert_page_meta(page_response, expected_total_elements=len(replies), expected_current_page=0)

            with allure.step("Verify first reply is the newly created sub-comment"):
                assert_comment_response(
                    replies[0],
                    self.eco_news_comment_client.get_comment_by_id(another_sub_comment_id).json()
                )

        with allure.step("Verify replies sorted by modifiedDate descending"):
            sort_params = ["modifiedDate,desc"]
            query = CommentQuery(page=0, size=20, sort=sort_params)
            page_response = self.eco_news_comment_client.get_active_replies(
                parent_comment_id=comment_id_with_images,
                query=query
            ).json()

            replies = page_response["page"]
            self.assert_sorted_by_date(replies, "modifiedDate", descending=True)
            assert_page_meta(page_response, expected_total_elements=len(replies), expected_current_page=0)

            with allure.step("Verify last reply corresponds to the original sub-comment"):
                assert_comment_response(
                    replies[-1],
                    self.eco_news_comment_client.get_comment_by_id(sub_comment_id).json()
                )

        with allure.step("Verify replies sorted by createdDate + modifiedDate descending"):
            sort_params = ["createdDate,desc", "modifiedDate,desc"]
            query = CommentQuery(page=0, size=20, sort=sort_params)
            page_response = self.eco_news_comment_client.get_active_replies(
                parent_comment_id=comment_id_with_images,
                query=query
            ).json()

            replies = page_response["page"]
            self.assert_sorted_by_date(replies, "createdDate", descending=True)
            self.assert_sorted_by_date(replies, "modifiedDate", descending=True)
            assert_page_meta(page_response, expected_total_elements=len(replies), expected_current_page=0)

            with allure.step("Verify middle reply is the sub-comment with images"):
                assert_comment_response(
                    replies[1],
                    self.eco_news_comment_client.get_comment_by_id(sub_comment_id_with_images).json()
                )
