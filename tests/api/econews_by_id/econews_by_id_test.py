import pytest
import allure
from allure_commons.types import Severity
import pytest_check as check

from clients.eco_news_client import EcoNewsClient
from data.config import Config
from data.eco_news_factory import EcoNewsUpdateFactory, create_news_uk, TEST_TAGS, TITLE_UK, CONTENT_UK, SOURCE_UK
from data.ui_news_test_data import TEST2_FILE
from enums.news_tag import EcoNewsTag
from models.update_eco_news_request import UpdateEcoNewsRequest
from tests.utils.api_test_assertions import assert_unauthorized, assert_ok, assert_not_found, assert_bad_request
from tests.utils.econews_assertions import assert_eco_news_response


@allure.epic("EcoNews API")
@allure.feature("EcoNews CRUD without authorization")
@allure.tag("EcoNewsById API")
@allure.severity(Severity.NORMAL)
class TestUnauthorizedEcoNewsById:
    """Tests for EcoNews API endpoints without authorization."""

    @allure.story("Update EcoNews without token")
    @allure.description("Verify that updating EcoNews without authorization returns 401 status code.")
    def test_update_eco_news_by_id_without_token(self, eco_news_setup):
        """ Test updating an EcoNews item without providing an authorization token. """
        client = eco_news_setup["client"]
        eco_news_id = eco_news_setup["eco_news_id"]
        update_dto = UpdateEcoNewsRequest(
            id=eco_news_id,
            title="Another string",
            content="Test content with more than 20 chars",
            short_info="Short info",
            tags=[]
        )
        response = client.update_eco_news_by_id(eco_news_id, update_dto)
        assert_unauthorized(response)

    @allure.story("Delete EcoNews without token")
    @allure.description("Verify that deleting EcoNews without authorization returns 401 status code.")
    def test_delete_eco_news_by_id_without_token(self, eco_news_setup):
        """ Test deleting an EcoNews item without providing an authorization token. """
        client = eco_news_setup["client"]
        eco_news_id = eco_news_setup["eco_news_id"]
        response = client.delete_eco_news_by_id(eco_news_id)
        assert_unauthorized(response)


@allure.epic("EcoNews API")
@allure.feature("Update EcoNews without image and Delete EcoNews")
@allure.tag("EcoNewsById API")
@allure.severity(Severity.NORMAL)
class TestEcoNewsById:
    """Test suite for EcoNews API operations by ID, including update and delete."""

    @allure.story("Update EcoNews without image")
    @allure.description("Verify that updating EcoNews without providing an image works correctly")
    def test_update_eco_news_by_id_without_image(self, created_eco_news_without_image_cleanup):
        """ Test for updating EcoNews without providing an image. """
        client: EcoNewsClient = created_eco_news_without_image_cleanup["client"]
        eco_news_id: int = created_eco_news_without_image_cleanup["eco_news_id"]

        dto_factory = EcoNewsUpdateFactory(eco_news_id)
        update_dto: UpdateEcoNewsRequest = dto_factory.update_dto_uk()

        response = client.update_eco_news_by_id(eco_news_id, update_dto)
        assert_ok(response)

        response_json = response.json()

        expected_data = {
            "id": eco_news_id,
            "title": update_dto.title,
            "content": update_dto.content,
            "shortInfo": update_dto.short_info,
            "tagsEn": update_dto.get_tags_en(),
            "tagsUk": update_dto.get_tags_uk(),
            "author": None,
            "imagePath": None,
            "source": update_dto.source
        }

        assert_eco_news_response(
            actual=response_json,
            expected=expected_data,
            check_image=False,
            check_author=False
        )

        check.is_false(response_json.get("hidden", False), "Hidden should be False")
        check.equal(response_json.get("likes", 0), 0, "Likes should be 0")
        check.equal(response_json.get("dislikes", 0), 0, "Dislikes should be 0")
        check.equal(response_json.get("countComments", 0), 0, "CountComments should be 0")

    @allure.story("Delete existing EcoNews")
    @allure.description(
        "Verify that an authorized user can successfully delete an existing EcoNews item"
    )
    def test_delete_eco_news_by_id(self, created_eco_news_without_image):
        """ Test deleting an existing EcoNews item by ID. """
        client = created_eco_news_without_image["client"]
        eco_news_id = created_eco_news_without_image["eco_news_id"]

        delete_response = client.delete_eco_news_by_id(eco_news_id)
        assert_ok(delete_response)

        get_response = client.get_eco_news_by_id(eco_news_id)
        assert_not_found(
            get_response,
            f"Eco new doesn't exist by this id: {eco_news_id}"
        )

    @allure.story("Delete non-existing EcoNews")
    @allure.description(
        "Verify that deleting a non-existing EcoNews returns 404 Not Found"
    )
    def test_delete_non_existing_eco_news_should_return_404(self, created_eco_news_without_image):
        """ Test deleting a non-existing EcoNews item by ID. """
        client = created_eco_news_without_image["client"]
        eco_news_id = created_eco_news_without_image["eco_news_id"]

        non_existing_id = eco_news_id + 10

        delete_response = client.delete_eco_news_by_id(non_existing_id)

        assert_not_found(
            delete_response,
            f"Eco new doesn't exist by this id: {non_existing_id}"
        )


@allure.epic("EcoNews API")
@allure.feature("CRUD operations with created news with image")
@allure.tag("EcoNewsById API")
@allure.severity(Severity.NORMAL)
class TestEcoNewsByIdWithImage:
    """ Test suite for verifying CRUD operations on EcoNews items with images. """

    @allure.story("Get EcoNews by ID")
    @allure.description("Verify that EcoNews can be successfully retrieved by ID.")
    def test_get_eco_news_by_id(self, created_eco_news):
        """ Test retrieving a specific EcoNews item by its ID. """
        client = created_eco_news["client"]
        eco_news_id = created_eco_news["eco_news_id"]
        response = client.get_eco_news_by_id(eco_news_id)
        assert_ok(response)
        eco_news = response.json()

        expected_data = {
            "id": eco_news["id"],
            "title": eco_news["title"],
            "content": eco_news["content"],
            "shortInfo": eco_news.get("shortInfo"),
            "tagsEn": eco_news.get("tagsEn", []),
            "tagsUk": eco_news.get("tagsUk", []),
            "author": eco_news.get("author"),
            "imagePath": eco_news.get("imagePath"),
        }

        assert_eco_news_response(
            actual=eco_news,
            expected=expected_data,
            check_image=bool(expected_data["imagePath"]),
            check_author=bool(expected_data.get("author"))
        )

    @allure.story("Get EcoNews in English and Ukrainian")
    @allure.description("Verify that EcoNews can be retrieved in English and Ukrainian using lang parameter.")
    @pytest.mark.parametrize("lang, message", [
        ("en", "Title in English should not be null"),
        ("uk", "Title in Ukrainian should not be null")
    ])
    def test_get_eco_news_by_lang(self, created_eco_news, lang, message):
        """ Test retrieving EcoNews titles in multiple languages. """
        client = created_eco_news["client"]
        eco_news_id = created_eco_news["eco_news_id"]
        response = client.get_eco_news_by_id_with_lang(eco_news_id, lang)
        assert_ok(response)
        eco_news = response.json()
        assert eco_news.get("title") is not None, message

    @allure.story("Get non-existing EcoNews")
    @allure.description("Verify that requesting a non-existing EcoNews returns 404 status code.")
    def test_get_non_existing_eco_news_should_return_404(self, created_eco_news):
        """ Test that attempting to fetch a non-existing EcoNews returns 404 Not Found. """
        client = created_eco_news["client"]
        non_existing_eco_news_id = created_eco_news["eco_news_id"] + 1
        response = client.get_eco_news_by_id(non_existing_eco_news_id)
        expected_message = f"Eco new doesn't exist by this id: {non_existing_eco_news_id}"
        assert_not_found(response, expected_message)

    @allure.story("Update EcoNews with invalid id, tag, title, content")
    @allure.description(
        "Verify that updating EcoNews with invalid id, tag, title, content returns 400 Bad Request"
    )
    def test_update_eco_news_by_id_should_return_400(self, created_eco_news_without_image_cleanup):
        """Test updating EcoNews with invalid ID, tags, title, or content."""
        client = created_eco_news_without_image_cleanup["client"]

        first_news_request = create_news_uk()
        first_news_response = client.post_eco_news(first_news_request)
        first_news = first_news_response.json()

        second_news_request = create_news_uk()
        second_news_response = client.post_eco_news(second_news_request)
        second_news = second_news_response.json()

        tags = EcoNewsTag.get_ua(TEST_TAGS)

        update_dto = UpdateEcoNewsRequest(
            id=second_news["id"],
            title=TITLE_UK,
            content=CONTENT_UK,
            short_info="Short info",
            tags=tags,
            source=SOURCE_UK
        )
        response = client.update_eco_news_by_id(first_news["id"], update_dto)
        assert_bad_request(
            response,
            "Eco news id in path param and eco news id in entity not equal"
        )

        update_dto.id = second_news["id"]
        update_dto.tags = ["string"]
        response = client.update_eco_news_by_id(second_news["id"], update_dto)
        assert_bad_request(response, "There should be at least one valid tag")

        update_dto.tags = tags
        update_dto.title = ""
        response = client.update_eco_news_by_id(second_news["id"], update_dto)
        assert_bad_request(response, ["must not be empty", "size must be between 1 and 170"])

        update_dto.title = TITLE_UK
        update_dto.content = ""
        response = client.update_eco_news_by_id(second_news["id"], update_dto)
        assert_bad_request(response, ["must not be empty", "size must be between 20 and 63206"])

    @allure.story("Update EcoNews by ID with image")
    @allure.description("Verify that updating EcoNews with a specific image is successful")
    def test_update_eco_news_by_id_with_image(self, created_eco_news):
        """ Test updating an EcoNews item with an image and verify response matches expected values. """
        client: EcoNewsClient = created_eco_news["client"]
        eco_news_id: int = created_eco_news["eco_news_id"]

        dto_factory = EcoNewsUpdateFactory(eco_news_id)
        update_dto: UpdateEcoNewsRequest = dto_factory.update_dto_uk()

        response = client.update_eco_news_by_id(eco_news_id, update_dto, str(TEST2_FILE))
        assert_ok(response)

        response_json = response.json()

        expected_data = {
            "id": eco_news_id,
            "title": update_dto.title,
            "content": update_dto.content,
            "shortInfo": update_dto.short_info,
            "tagsEn": update_dto.get_tags_en(),
            "tagsUk": update_dto.get_tags_uk(),
            "author": None,
            "imagePath": response_json.get("imagePath"),
            "source": update_dto.source
        }

        assert_eco_news_response(
            actual=response_json,
            expected=expected_data,
            check_image=True,
            check_author=False
        )

        check.is_false(response_json.get("hidden", False), "Hidden should be False")
        check.equal(response_json.get("likes", 0), 0, "Likes should be 0")
        check.equal(response_json.get("dislikes", 0), 0, "Dislikes should be 0")
        check.equal(response_json.get("countComments", 0), 0, "CountComments should be 0")


@allure.epic("EcoNews API")
@allure.feature("Count likes on EcoNews by ID")
@allure.tag("EcoNewsById API")
@allure.severity(Severity.NORMAL)
class TestEcoNewsByIdLikes:
    """Test suite for verifying the likes count and like actions on EcoNews by ID."""

    @allure.story("Get likes count for EcoNews by ID")
    @allure.description(
        "Verify that retrieving the likes count for an EcoNews item by ID "
        "is successful."
    )
    def test_count_eco_news_likes(self, created_eco_news):
        """
        Verify that the API returns the correct response when requesting
        the number of likes for an EcoNews item by its ID.
        """
        client = created_eco_news["client"]
        eco_news_id = created_eco_news["eco_news_id"]

        response = client.count_eco_news_likes(eco_news_id)
        assert_ok(response)

        body = response.text.strip()

        with allure.step("Verify response body is an integer"):
            assert body.lstrip("-").isdigit(), f"Response body is not an integer: {body}"

    @allure.story("Get likes count for non-existing EcoNews")
    @allure.description(
        "Verify that an attempt to get likes count for a non-existing EcoNews item "
        "returns 404 Not Found."
    )
    def test_count_non_existing_eco_news_likes_should_return_404(self, eco_news_setup):
        """
        Verify that the API returns 404 when requesting likes count
        for a non-existing EcoNews ID.
        """
        client = eco_news_setup["client"]
        non_existing_id = eco_news_setup["eco_news_id"] + 10
        response = client.count_eco_news_likes(non_existing_id)
        expected_message = f"Eco new doesn't exist by this id: {non_existing_id}"
        assert_not_found(response, expected_message)

    @allure.story("Count likes with invalid input")
    @allure.description(
        "Verify that providing invalid input to count_eco_news_likes returns 400 Bad Request.")
    def test_count_eco_news_likes_should_return_400(self, refresh_auth_token):
        """Check that API returns 400 Bad Request when likes count is requested with invalid ID."""
        client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=refresh_auth_token)
        invalid_id = "invalid_id"
        response = client.count_eco_news_likes(invalid_id)
        expected_message = "Wrong ecoNewsId. Should be 'Long'"
        assert_bad_request(response, expected_message)

    @allure.story("Like non-existing EcoNews")
    @allure.description(
        "Verify that an attempt to like a non-existing EcoNews item "
        "returns 404 Not Found."
    )
    def test_like_non_existing_eco_news_by_id_should_return_404(self, refresh_auth_token, eco_news_setup):
        """
        Verify that the API returns 404 when trying to like
        a non-existing EcoNews item.
        """
        client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=refresh_auth_token)
        non_existing_id = eco_news_setup["eco_news_id"] + 10
        response = client.like_eco_news_by_id(non_existing_id)
        expected_message = f"Eco new doesn't exist by this id: {non_existing_id}"
        assert_not_found(response, expected_message)

    @allure.story("Like another user's EcoNews")
    @allure.description(
        "Verify that an attempt to like EcoNews created by another user "
        "is successful."
    )
    def test_like_another_users_eco_news_by_id(self, refresh_auth_token, created_eco_news_second_user):
        """ Verify that a user can like EcoNews created by another user. """
        client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=refresh_auth_token)
        another_user_eco_news_id = created_eco_news_second_user["eco_news_id"]
        response = client.like_eco_news_by_id(another_user_eco_news_id)
        assert_ok(response)

    @allure.story("Like EcoNews without token")
    @allure.description(
        "Verify that an attempt to like EcoNews without being authorized "
        "returns 401 status code."
    )
    def test_like_another_users_eco_news_by_id_without_token(
            self, eco_news_setup, created_eco_news_second_user
    ):
        """Verify that liking EcoNews without an access token returns 401."""
        client = eco_news_setup["client"]
        eco_news_id = created_eco_news_second_user["eco_news_id"]
        response = client.like_eco_news_by_id(eco_news_id)
        assert_unauthorized(response)

    @allure.story("Like own EcoNews")
    @allure.description(
        "Verify that an attempt to like a user's own EcoNews returns 400 Bad Request "
        "with the correct error message."
    )
    def test_like_own_eco_news_should_return_400(self, created_eco_news):
        """Verify that a user cannot like their own EcoNews."""
        client = created_eco_news["client"]
        eco_news_id = created_eco_news["eco_news_id"]
        response = client.like_eco_news_by_id(eco_news_id)
        expected_message = "Current user has no permission for this action"
        assert_bad_request(response, expected_message)
