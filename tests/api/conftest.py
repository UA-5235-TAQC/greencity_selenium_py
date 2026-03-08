from typing import Generator, List

import allure
from pytest import fixture, FixtureRequest

from clients.eco_news_client import EcoNewsClient
from clients.eco_news_comment_client import EcoNewsCommentClient
from clients.own_security_client import OwnSecurityClient
from data.comment_factory import parent_comment, comment_with_images, PARENT_SUB_COMMENT, sub_comment_with_images, \
    sub_comment
from data.eco_news_factory import create_news_uk
from data.config import Config
from data.ui_news_test_data import TEST_FILE, TEST2_FILE, SMALL_PNG_IMAGE
from models.eco_news_request import EcoNewsRequest
from tests.api.utils.api_test_assertions import assert_ok, assert_created
from utils.logging_config import AllureStepLogger

AllureStepLogger.setup_logging()


@fixture(scope="session")
def worker_id(request: FixtureRequest) -> str:
    """Return the pytest-xdist worker identifier, or ``"master"`` for serial runs.
    """
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


@fixture(scope="session")
def eco_news_setup():
    """Fixture to prepare EcoNews client and fetch first EcoNews item."""
    eco_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=None)
    response = eco_news_client.get_eco_news({"page": 0, "size": 10})
    page_response = response.json()
    first_news = page_response["page"][0]
    eco_news_id = first_news["id"]
    return {"client": eco_news_client, "eco_news_id": eco_news_id}


@fixture(scope="session")
def _auth_tokens():
    """Obtain and store the initial access + refresh token pair for the session."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
    assert_ok(login_response)
    body = login_response.json()
    return {
        "access_token": body["accessToken"],
        "refresh_token": body.get("refreshToken", ""),
    }


@fixture(scope="session")
def auth_token(_auth_tokens):
    """Get auth token."""
    return _auth_tokens["access_token"]


@fixture(scope="function")
def refresh_auth_token(_auth_tokens):
    """Return a freshly-obtained access token by exchanging the refresh token."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    refresh_response = auth_client.refresh_token(_auth_tokens["refresh_token"])

    if refresh_response.status_code == 200:
        body = refresh_response.json()
        _auth_tokens["access_token"] = body["accessToken"]
        _auth_tokens["refresh_token"] = body.get("refreshToken", _auth_tokens["refresh_token"])
    else:
        allure.attach(
            f"status={refresh_response.status_code} body={refresh_response.text[:500]}",
            name="refresh_token failure details",
        )
        with allure.step(
                f"Refresh token failed (HTTP {refresh_response.status_code}); performing full re-login"
        ):
            login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
            assert_ok(login_response)
            body = login_response.json()
            _auth_tokens["access_token"] = body["accessToken"]
            _auth_tokens["refresh_token"] = body.get("refreshToken", "")

    return _auth_tokens["access_token"]


@fixture(scope="session")
def comments_client_second_user():
    """Provide EcoNewsCommentClient authorized as the second user."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_resp = auth_client.sign_in(Config.SECOND_USER_EMAIL, Config.SECOND_USER_PASSWORD)
    assert_ok(login_resp)
    access_token = login_resp.json()["accessToken"]
    return EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, access_token=access_token)


@fixture(scope="module")
def created_eco_news_without_image(auth_token):
    """Create EcoNews and print it to console."""
    client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)
    news_dto: EcoNewsRequest = create_news_uk()
    response = client.post_eco_news(news_dto)

    assert_created(response)

    created_news = response.json()

    return {"client": client, "eco_news_id": created_news["id"], "news": created_news}


@fixture(scope="module")
def created_eco_news_without_image_cleanup(created_eco_news_without_image):
    """Create EcoNews and delete it after all tests in the module."""
    yield created_eco_news_without_image
    client = created_eco_news_without_image["client"]
    eco_news_id = created_eco_news_without_image["eco_news_id"]
    client.delete_eco_news_by_id(eco_news_id)


@fixture(scope="module")
def created_eco_news(auth_token):
    """Create EcoNews with image."""
    client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)

    news_dto = create_news_uk()

    response = client.post_eco_news_with_image(news_dto, str(TEST_FILE))

    assert_created(response)

    news = response.json()
    eco_news_id = news["id"]

    yield {"client": client, "eco_news_id": eco_news_id, "news": news}

    client.delete_eco_news_by_id(eco_news_id)


@fixture(scope="function")
def auth_client_favorite(refresh_auth_token, created_eco_news_without_image_cleanup):
    """
    Provide authorized EcoNews client with a news item prepared for favorite tests.
    Ensures the news is not in favorites before and after the test.
    """
    client = EcoNewsClient(
        Config.BASE_GREEN_CITY_API_URL,
        access_token=refresh_auth_token
    )

    news_id = created_eco_news_without_image_cleanup["eco_news_id"]

    with allure.step(f"Pre-test cleanup: remove news {news_id} from favorites"):
        try:
            client.remove_from_favorites(news_id)
        except Exception as exc:  # noqa: BLE001
            allure.attach(str(exc), name="Pre-test cleanup failed")

    yield {"client": client, "news_id": news_id}

    with allure.step(f"Post-test cleanup: remove news {news_id} from favorites"):
        try:
            client.remove_from_favorites(news_id)
        except Exception as exc:  # noqa: BLE001
            allure.attach(str(exc), name="Post-test cleanup failed")


@fixture(scope="class")
def create_comments(request, auth_token, created_eco_news_without_image):
    """
    Create a set of comments for the test class using EcoNewsCommentClient.
    The fixture creates:
    - one parent comment
    - one parent comment with images
    - a sub-comment for the parent comment
    - a sub-comment for the comment with images
    - a sub-comment with images
    """
    news_id = created_eco_news_without_image["eco_news_id"]

    client = EcoNewsCommentClient(
        base_url=created_eco_news_without_image["client"].base_api_url,
        access_token=auth_token,
        news_id=news_id
    )

    created_comment_ids: List[int] = []

    with allure.step("Create parent comment"):
        parent_comment_resp = client.add_comment(parent_comment(), parent_comment_id=0)
        assert_created(parent_comment_resp)

        parent_comment_id = parent_comment_resp.json()["id"]
        created_comment_ids.append(parent_comment_id)

    with allure.step("Create parent comment with images"):
        comment_with_images_resp = client.add_comment(
            comment_with_images(),
            parent_comment_id=0,
            image_paths=[str(TEST_FILE), str(TEST2_FILE)]
        )
        assert_created(comment_with_images_resp)

        comment_id_with_images = comment_with_images_resp.json()["id"]
        created_comment_ids.append(comment_id_with_images)

    with allure.step("Create sub-comment for parent comment with image"):
        parent_sub_comment_resp = client.add_comment(
            PARENT_SUB_COMMENT,
            parent_comment_id=parent_comment_id,
            image_paths=[str(SMALL_PNG_IMAGE)]
        )
        assert_created(parent_sub_comment_resp)

        parent_sub_comment_id = parent_sub_comment_resp.json()["id"]
        created_comment_ids.append(parent_sub_comment_id)

    with allure.step("Create sub-comment for comment with images"):
        sub_comment_resp = client.add_comment(
            sub_comment(),
            parent_comment_id=comment_id_with_images
        )
        assert_created(sub_comment_resp)

        sub_comment_id = sub_comment_resp.json()["id"]
        created_comment_ids.append(sub_comment_id)

    with allure.step("Create sub-comment with images for comment with images"):
        sub_comment_with_images_resp = client.add_comment(
            sub_comment_with_images(),
            parent_comment_id=comment_id_with_images,
            image_paths=[str(TEST_FILE), str(TEST2_FILE)]
        )
        assert_created(sub_comment_with_images_resp)

        sub_comment_id_with_images = sub_comment_with_images_resp.json()["id"]
        created_comment_ids.append(sub_comment_id_with_images)

    with allure.step("Attach created comment data to the test class"):
        request.cls.eco_news_comment_client = client
        request.cls.created_comment_ids = created_comment_ids
        request.cls.parent_comment_id = parent_comment_id
        request.cls.comment_id_with_images = comment_id_with_images
        request.cls.parent_sub_comment_id = parent_sub_comment_id
        request.cls.sub_comment_id = sub_comment_id
        request.cls.sub_comment_id_with_images = sub_comment_id_with_images

    yield

    with allure.step("Delete parent comments with all their child comments"):
        for cid in [parent_comment_id, comment_id_with_images]:
            client.delete_comment_with_children(cid)


@fixture(scope="function")
def create_comment_with_token(created_eco_news, auth_token) -> Generator[tuple[str, int, dict], None, None]:
    """
    Fixture: create a comment using API.
    Returns:
        token (str): authentication token used for API requests
        news_id (int): ID of the news to which the comment was added
        comment_response (dict): created comment response data
    """

    token = auth_token
    news_id = created_eco_news["eco_news_id"]

    comment_client = EcoNewsCommentClient(
        Config.BASE_GREEN_CITY_API_URL,
        token,
        news_id
    )

    response = comment_client.add_comment(
        text="This is a test comment.",
        parent_comment_id=0,
        image_paths=[str(TEST2_FILE)]
    )

    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"

    yield token, news_id, response.json()


@fixture(scope="function")
def create_and_cleanup_comment(create_comment_with_token) -> Generator[tuple[dict, EcoNewsCommentClient], None, None]:
    """
    Fixture: create a comment using API and delete it after test.
    Returns:
    - token: str - the authentication token used for API requests
    - comment_response: dict - the response data of the created comment, including its ID and
    """

    token, news_id, comment_response = create_comment_with_token
    comments_client = EcoNewsCommentClient(Config.BASE_GREEN_CITY_API_URL, token, news_id)
    yield comment_response, comments_client

    delete_response = comments_client.delete_comment_by_id(comment_response["id"])
    assert delete_response.status_code == 200, f"Expected status code 200, but got {delete_response.status_code}"
