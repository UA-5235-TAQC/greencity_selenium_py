from typing import Generator
import allure
from allure_commons.types import Severity
from pytest import fixture, FixtureRequest
import requests
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from clients.eco_news_client import EcoNewsClient
from clients.eco_news_comment_client import EcoNewsCommentClient
from clients.own_security_client import OwnSecurityClient
from data.comment_factory import (parent_comment, comment_with_images,
                                  PARENT_SUB_COMMENT, sub_comment_with_images, sub_comment)
from data.eco_news_factory import create_news_uk
from data.config import Config
from data.ui_news_test_data import (TEST_FILE, TEST2_FILE,
                                    SMALL_PNG_IMAGE, apply_to_en, apply_to_ua)
from models.eco_news_request import EcoNewsRequest
from tests.utils.api_test_assertions import assert_ok, assert_created
from utils.logging_config import AllureStepLogger

from components.news_list_item_component import NewsListItemComponent
from enums.language import Language
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.home_page import HomePage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage

AllureStepLogger.setup_logging()


@fixture(scope="session")
def worker_id(request: FixtureRequest) -> str:
    """Return the pytest-xdist worker identifier, or ``"master"`` for serial runs."""
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
        except requests.RequestException as exc:
            allure.attach(str(exc), name="Pre-test cleanup failed")

    yield {"client": client, "news_id": news_id}

    with allure.step(f"Post-test cleanup: remove news {news_id} from favorites"):
        try:
            client.remove_from_favorites(news_id)
        except requests.RequestException as exc:
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

    comment_ids = {}

    with allure.step("Create parent comment"):
        resp = client.add_comment(parent_comment(), parent_comment_id=0)
        assert_created(resp)
        comment_ids["parent"] = resp.json()["id"]

    with allure.step("Create parent comment with images"):
        resp = client.add_comment(
            comment_with_images(),
            parent_comment_id=0,
            image_paths=[str(TEST_FILE), str(TEST2_FILE)]
        )
        assert_created(resp)
        comment_ids["with_images"] = resp.json()["id"]

    with allure.step("Create sub-comment for parent comment with image"):
        resp = client.add_comment(
            PARENT_SUB_COMMENT,
            parent_comment_id=comment_ids["parent"],
            image_paths=[str(SMALL_PNG_IMAGE)]
        )
        assert_created(resp)
        comment_ids["parent_sub"] = resp.json()["id"]

    with allure.step("Create sub-comment for comment with images"):
        resp = client.add_comment(
            sub_comment(),
            parent_comment_id=comment_ids["with_images"]
        )
        assert_created(resp)
        comment_ids["sub"] = resp.json()["id"]

    with allure.step("Create sub-comment with images for comment with images"):
        resp = client.add_comment(
            sub_comment_with_images(),
            parent_comment_id=comment_ids["with_images"],
            image_paths=[str(TEST_FILE), str(TEST2_FILE)]
        )
        assert_created(resp)
        comment_ids["sub_with_images"] = resp.json()["id"]

    request.cls.eco_news_comment_client = client
    request.cls.comment_ids = comment_ids

    yield

    with allure.step("Delete parent comments with all their child comments"):
        for cid in [comment_ids["parent"], comment_ids["with_images"]]:
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


@fixture(scope="function", params=["chrome"])
def get_driver(request):
    """ Pytest fixture that initializes and provides a Selenium WebDriver instance. """
    allure.dynamic.parameter("browser", request.param)
    browser = request.param
    headless = Config.HEADLESS_MODE

    driver = None

    match browser:
        case "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            driver = Chrome(options=options)  # pylint: disable=not-callable
        case "firefox":

            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            driver = Firefox(options=options)  # pylint: disable=not-callable
    driver.implicitly_wait(Config.IMPLICITLY_WAIT)
    driver.get(Config.BASE_UI_GREEN_CITY_URL)

    yield driver

    driver.quit()


@fixture(scope="function")
def driver_with_login(get_driver):
    """Fixture that logs in the user before yielding the driver."""

    allure.dynamic.severity(Severity.CRITICAL)

    sign_in_modal = HomePage(get_driver).open().header.change_to_en().click_sign_in_link()

    sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    yield get_driver

    get_driver.delete_all_cookies()


@fixture(scope="function")
def eco_page(driver_with_login) -> Generator[NewsPage, None, None]:
    """ Fixture that opens the EcoNews page after login. """
    eco_news_page = NewsPage(driver_with_login).open()
    assert eco_news_page.is_page_opened(), "EcoNews page should be opened"
    yield eco_news_page

    eco_news_page.remove_all_selected_tags()


@fixture(scope="function")
def go_to_create_news_page(driver_with_login) -> CreateNewsPage:
    """ Fixture: open Create News page. """
    header = HomePage(driver_with_login).header
    create_news_page: CreateNewsPage = header.click_news_link().click_create_news()
    assert create_news_page.is_page_opened(), "Create News page should be opened"
    return create_news_page


@fixture(scope="function")
def eco_news_details_page(driver_with_login, go_to_create_news_page) -> NewsDetailsPage:
    """ Fixture: create a news item, open its news details page. """
    apply_to_en(go_to_create_news_page)
    eco_news_page = go_to_create_news_page.click_publish()
    news_card: NewsListItemComponent = eco_news_page.get_news_card_by_index(0)
    news_details_page: NewsDetailsPage = news_card.click_image()
    assert news_details_page.is_page_opened(), "News details page should be opened"
    return news_details_page


@fixture(scope="function", params=[Language.EN, Language.UK])
def edit_news_page_with_language(driver_with_login, go_to_create_news_page, request) -> EditNewsPage:
    """
    Fixture: create a news item, open its edit page, and return EditNewsPage.
    Param `request.param` is 'en' or 'ua'.
    """
    language = request.param
    if language == Language.EN:
        go_to_create_news_page.header.change_to_en()
        apply_to_en(go_to_create_news_page)
    else:
        go_to_create_news_page.header.change_to_uk()
        apply_to_ua(go_to_create_news_page)

    eco_news_page: NewsPage = go_to_create_news_page.click_publish()
    if language == Language.EN:
        eco_news_page.header.change_to_en()
    else:
        eco_news_page.header.change_to_uk()

    news_card: NewsListItemComponent = eco_news_page.get_news_card_by_index(0)
    news_details_page: NewsDetailsPage = news_card.click_image()
    assert news_details_page.is_page_opened(), "News details page should be opened"

    if language == Language.EN:
        news_details_page.header.change_to_en()
    else:
        news_details_page.header.change_to_uk()

    news_details_page.click_edit_button()
    eco_news_id = news_details_page.get_news_id()

    edit_news_page = EditNewsPage(driver_with_login, eco_news_id)
    assert edit_news_page.is_page_opened(), "Edit News page should be opened"
    return edit_news_page


@fixture(scope="function")
def tag_selection_environment(driver_with_login):
    """Prepare environment for tag selection tests."""
    driver = driver_with_login
    news_page = NewsPage(driver).open()
    news_page.header.change_to_en()
    create_news_page: CreateNewsPage = news_page.click_create_news()
    yield create_news_page, news_page
    news_page.open()
    news_page.remove_all_selected_tags()


@fixture(scope="function")
def news_created_by_second_user(get_driver) -> Generator[int, None, None]:
    """Fixture: login as second user, create news and open its details page."""

    driver = get_driver

    with allure.step("Login as second user"):
        sign_in_modal = HomePage(driver).open().header.change_to_en().click_sign_in_link()
        sign_in_modal.sign_in(Config.SECOND_USER_EMAIL, Config.SECOND_USER_PASSWORD)

    with allure.step("Open Create News page"):
        create_news_page: CreateNewsPage = HomePage(driver).header.click_news_link().click_create_news()
        assert create_news_page.is_page_opened(), "Create News page should be opened"

    with allure.step("Create news as second user"):
        apply_to_en(create_news_page)
        eco_news_page = create_news_page.click_publish()

    with allure.step("Open created news details page"):
        news_card: NewsListItemComponent = eco_news_page.get_news_card_by_index(0)
        news_details_page: NewsDetailsPage = news_card.click_image()
        assert news_details_page.is_page_opened(), "News details page should be opened"

    news_id = news_details_page.get_news_id()

    with allure.step("Logout second user"):
        dropdown = news_details_page.header.click_profile_dropdown()
        dropdown.sign_out()

    with allure.step("Login as first user"):
        sign_in_modal = HomePage(driver).open().header.change_to_en().click_sign_in_link()
        sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    yield news_id

    with allure.step("Logout first user"):
        dropdown = news_details_page.header.click_profile_dropdown()
        dropdown.sign_out()

    with allure.step("Login as second user"):
        sign_in_modal = HomePage(get_driver).open().header.change_to_en().click_sign_in_link()
        sign_in_modal.sign_in(Config.SECOND_USER_EMAIL, Config.SECOND_USER_PASSWORD)

    with allure.step("Delete created news"):
        news_details_page = NewsDetailsPage(get_driver).open(news_id)
        news_details_page.delete_news_by_id(news_id)

    with allure.step("Clear cookies after test"):
        driver.delete_all_cookies()
