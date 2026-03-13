import allure
from allure_commons.types import Severity
from clients.eco_news_comment_client import EcoNewsCommentClient
from clients.eco_news_client import EcoNewsClient
from data.comment_factory import COMMENT_MESSAGE, COMMENT_UPDATE_MESSAGE
from data.config import Config
from data.ui_news_test_data import TEST2_FILE
from schemas.greencity.comment import comment_schema
from tests.utils.api_test_assertions import assert_ok, assert_created
from tests.utils.validators import validate_json


@allure.epic("EcoNewsComments API")
@allure.feature("EcoNewsComments Management")
@allure.story("Get News Comments Count")
@allure.title("Verify comments count increases after adding a comment")
@allure.tag("EcoNewsComments API")
@allure.severity(Severity.NORMAL)
def test_get_news_comments_count(create_and_cleanup_comment):
    """Verify that the comments count for a news item increases after adding a new comment."""
    comment_response, comments_client = create_and_cleanup_comment
    news_id = comments_client.news_id

    with allure.step("Get comments count response and verify status code"):
        response = comments_client.get_comments_count(news_id)
        assert_ok(response)

    with allure.step("Get comments count"):
        comments_count = response.json()

    with allure.step("Add a new comment"):
        response = comments_client.add_comment(text=COMMENT_MESSAGE)
        assert_created(response)

    with allure.step("Get updated comments count"):
        response = comments_client.get_comments_count(news_id)
        assert_ok(response)
        updated_comments_count = response.json()
        assert updated_comments_count == comments_count + 1, "Comments count should increment by 1"


@allure.epic("EcoNewsComments API")
@allure.feature("EcoNewsComments Reactions")
@allure.story("Dislike Comment")
@allure.title("Verify that a comment dislike status toggles correctly")
@allure.tag("EcoNewsComments API")
@allure.severity(Severity.NORMAL)
def test_dislike_comment(comments_client_second_user, create_and_cleanup_comment):
    """Verify that a comment dislike status toggles correctly by another user."""
    comment_response, _ = create_and_cleanup_comment
    comment_id = comment_response["id"]

    with allure.step("Get comment by id and verify status"):
        response = comments_client_second_user.get_comment_by_id(comment_id)
        assert_ok(response)

    with allure.step("Get dislikes status before"):
        dislikes_before = bool(response.json().get("dislikes", 0))

    with allure.step("Dislike comment"):
        response = comments_client_second_user.dislike_comment_and_get_instance(comment_id)
        assert_ok(response)

    with allure.step("Verify dislike status is updated"):
        dislikes_after = bool(response.json().get("dislikes", 0))
        assert dislikes_before != dislikes_after, "Dislike status should toggle"


@allure.epic("EcoNewsComments API")
@allure.feature("EcoNewsComments Management")
@allure.story("Update Comment")
@allure.title("Verify that a comment can be successfully updated")
@allure.tag("EcoNewsComments API")
@allure.severity(Severity.NORMAL)
def test_update_comment(create_and_cleanup_comment):
    """Verify that a comment can be successfully updated."""
    comment_response, comments_client = create_and_cleanup_comment
    comment_id = comment_response["id"]

    with allure.step("Update comment and verify status"):
        response = comments_client.update_comment(comment_id=comment_id, text=COMMENT_UPDATE_MESSAGE)
        assert_ok(response)

    with allure.step("Get comment by id and verify status"):
        response = comments_client.get_comment_by_id(comment_id=comment_id)
        assert_ok(response)

    with allure.step("Verify response body"):
        response = response.json()
        assert response["text"] == f'"{COMMENT_UPDATE_MESSAGE}"', "Response text should be equal to comment message"
        assert response["author"]["id"] == Config.USER_ID, "Author id should be equal to 149"
        assert response["author"]["name"] == Config.USER_NAME, "Author name should be equal to NameForTest611"


@allure.epic("EcoNewsComments API")
@allure.feature("EcoNewsComments Management")
@allure.tag("EcoNewsComments API")
class TestNewsComments:
    """API tests for EcoNews comments functionality."""

    @allure.title("Add comment to eco news")
    @allure.story("Create comment")
    @allure.description(
        "Verify that a user can successfully add a comment to an eco news item with an image."
    )
    @allure.severity(Severity.NORMAL)
    def test_add_comment_to_eco_news(self, created_eco_news_without_image_cleanup):
        """Test: Add a comment to eco news."""
        client: EcoNewsClient = created_eco_news_without_image_cleanup["client"]
        news_id: int = created_eco_news_without_image_cleanup["eco_news_id"]

        comment_client = EcoNewsCommentClient(
            Config.BASE_GREEN_CITY_API_URL,
            client.access_token,
            news_id
        )

        response = comment_client.add_comment(
            "This is a test comment.",
            image_paths=[str(TEST2_FILE)]
        )

        assert_created(response)

        is_valid, error = validate_json(response.json(), comment_schema)
        assert is_valid, f"Response JSON does not match the expected schema: {error}"

    @allure.title("Like comment")
    @allure.story("React to comment")
    @allure.description("Verify that a user can like a comment.")
    @allure.severity(Severity.NORMAL)
    def test_like_comment(self, create_and_cleanup_comment, comments_client_second_user):
        """Test: Like a comment."""
        comment_response, comments_client = create_and_cleanup_comment
        comment_id = comment_response["id"]
        comment_data = comments_client_second_user.get_comment_by_id(comment_id).json()
        likes = comment_data["likes"]

        with allure.step("Second user likes the comment"):
            response = comments_client_second_user.like_comment(comment_id)
            assert_ok(response)

        with allure.step("Verify that the like count increased / is registered"):
            new_comment_data = comments_client_second_user.get_comment_by_id(comment_id).json()
            assert new_comment_data["likes"] == likes + 1, "Comment should have one like"

    @allure.title("Get comment by ID")
    @allure.story("Retrieve comment")
    @allure.description("Verify that a comment can be retrieved by its ID.")
    @allure.severity(Severity.TRIVIAL)
    def test_get_comment_by_id(self, create_and_cleanup_comment):
        """Test: Get a comment by its ID."""
        comment_response, comment_client = create_and_cleanup_comment
        comment_id = comment_response["id"]
        response = comment_client.get_comment_by_id(comment_id)
        assert_ok(response)
        is_valid, error = validate_json(response.json(), comment_schema)
        assert is_valid, f"Response JSON does not match the expected schema: {error}"

    @allure.title("Delete comment by ID")
    @allure.story("Delete comment")
    @allure.description("Verify that a user can delete their comment by ID.")
    @allure.severity(Severity.TRIVIAL)
    def test_delete_comment_by_id(self, create_comment_with_token):
        """Test: Delete a comment by its ID."""
        access_token, _, comment_response = create_comment_with_token
        comment_id = comment_response["id"]
        comment_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token)
        response = comment_client.delete_comment_by_id(comment_id)
        assert_ok(response)
