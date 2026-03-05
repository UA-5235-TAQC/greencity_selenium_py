import allure

from clients.eco_news_comment_client import EcoNewsCommentClient
from data.config import Config

NEWS_ID = 4044
COMMENT_MESSAGE = "hello"
COMMENT_ID = 2627
COMMENT_ID_UPDATE = 2636


@allure.epic("APITests")
@allure.feature("Comments")
@allure.story("Get News Comments Count")
def test_get_news_comments_count(comments_client: EcoNewsCommentClient):
    comments_client.news_id = NEWS_ID

    with allure.step("Get comments count response and verify status code"):
        response = comments_client.get_comments_count(news_id=NEWS_ID)
        assert response.status_code == 200, "Response status code should be 200"

    with allure.step("Get comments count"):
        comments_count = response.json()

    with allure.step("Add a new comment"):
        response = comments_client.add_comment(text=COMMENT_MESSAGE)
        assert response.status_code == 201, "Response status code should be 201"

    with allure.step("Get updated comments count"):
        response = comments_client.get_comments_count(news_id=NEWS_ID)
        assert response.status_code == 200, "Response status code should be 200"
        updated_comments_count = response.json()
        assert updated_comments_count == comments_count + 1, "Comments count should increment by 1"


@allure.epic("APITests")
@allure.feature("Comments")
@allure.story("Dislike Comment")
def test_dislike_comment(comments_client: EcoNewsCommentClient):
    with allure.step("Get comment by id and verify status"):
        response = comments_client.get_comment_by_id(comment_id=COMMENT_ID)
        assert response.status_code == 200, "Response status code should be 200"

    with allure.step("Get dislikes status and verify response status code"):
        dislikes_before = bool(response.json()["dislikes"])

    with allure.step("Dislike comment and verify response status code"):
        response = comments_client.dislike_comment_and_get_instance(comment_id=COMMENT_ID)
        assert response.status_code == 200, "Response status code should be 200"

    with allure.step("Verify dislike status is updated"):
        dislikes_after = bool(response.json()["dislikes"])
        assert dislikes_before != dislikes_after, "The Results should not equal to each other"


@allure.epic("APITests")
@allure.feature("Comments")
@allure.story("Update Comment")
def test_update_comment(comments_client: EcoNewsCommentClient):
    with allure.step("Update comment and verify status"):
        response = comments_client.update_comment(comment_id=COMMENT_ID_UPDATE, text=COMMENT_MESSAGE)
        assert response.status_code == 200, "Response status code should be 200"

    with allure.step("Get comment by id and verify status"):
        response = comments_client.get_comment_by_id(comment_id=COMMENT_ID_UPDATE)
        assert response.status_code == 200, "Response status code should be 200"

    with allure.step("Verify response body"):
        response = response.json()
        assert response["text"] == f'"{COMMENT_MESSAGE}"', "Response text should be equal to comment message"
        assert response["author"]["id"] == Config.USER_ID, "Author id should be equal to 149"
        assert response["author"]["name"] == Config.USER_NAME, "Author name should be equal to NameForTest611"
