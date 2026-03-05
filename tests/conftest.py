from typing import Generator

import allure
from allure_commons.types import Severity
from requests import Response
from enums.news_tag import EcoNewsTag
from schemas.greencity_user.own_security import success_sign_in_schema
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from clients.own_security_client import OwnSecurityClient
from components.news_list_item_component import NewsListItemComponent
from data.config import Config
from data.ui_news_test_data import NewsTestData
from enums.language import Language
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.home_page import HomePage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage
from tests.utils.validators import validate_json
from clients.eco_news_client import EcoNewsClient


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
            driver = webdriver.Chrome(options=options)
        case "firefox":

            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(Config.IMPLICITLY_WAIT)
    driver.get(Config.BASE_UI_GREEN_CITY_URL)

    yield driver

    driver.quit()


@fixture(scope="function")
def driver_with_login(get_driver):
    """Fixture that logs in the user before yielding the driver."""

    allure.dynamic.severity(Severity.CRITICAL)

    sign_in_modal = (HomePage(get_driver).open().header.change_to_en().click_sign_in_link())

    sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    yield get_driver

    get_driver.delete_all_cookies()


@fixture(scope="function")
def sign_in_api():
    """Fixture that performs API sign-in and yields the response JSON containing the access token."""

    client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    response = client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    is_valid, error = validate_json(response.json(), success_sign_in_schema)
    assert is_valid, f"Response JSON does not match the expected schema: {error}"

    yield response.json()


@fixture(scope="function")
def eco_page(driver_with_login) -> Generator[NewsPage, None, None]:
    """ Fixture that opens the EcoNews page after login. """
    eco_page = NewsPage(driver_with_login).open()
    assert eco_page.is_page_opened(), "EcoNews page should be opened"
    yield eco_page

    eco_page.remove_all_selected_tags()


@fixture(scope="function")
def create_news_page(driver_with_login, request) -> CreateNewsPage:
    """ Fixture: open Create News page. """
    header = HomePage(driver_with_login).header
    create_news_page: CreateNewsPage = header.click_news_link().click_create_news()
    assert create_news_page.is_page_opened(), "Create News page should be opened"
    return create_news_page


@fixture(scope="function")
def eco_news_details_page(driver_with_login, create_news_page, request) -> NewsDetailsPage:
    """ Fixture: create a news item, open its news details page. """
    NewsTestData.apply_to_en(create_news_page)
    eco_news_page = create_news_page.click_publish()
    news_card: NewsListItemComponent = eco_news_page.get_news_card_by_index(0)
    news_details_page: NewsDetailsPage = news_card.click_image()
    assert news_details_page.is_page_opened(), "News details page should be opened"
    return news_details_page


@fixture(scope="function", params=[Language.EN, Language.UK])
def edit_news_page_with_language(driver_with_login, create_news_page, request) -> EditNewsPage:
    """
    Fixture: create a news item, open its edit page, and return EditNewsPage.
    Param `request.param` is 'en' or 'ua'.
    """
    language = request.param
    if language == Language.EN:
        create_news_page.header.change_to_en()
        NewsTestData.apply_to_en(create_news_page)
    else:
        create_news_page.header.change_to_uk()
        NewsTestData.apply_to_ua(create_news_page)

    eco_news_page = create_news_page.click_publish()
    eco_news_page.header.change_to_en() if language == Language.EN else eco_news_page.header.change_to_uk()

    news_card: NewsListItemComponent = eco_news_page.get_news_card_by_index(0)
    news_details_page: NewsDetailsPage = news_card.click_image()
    assert news_details_page.is_page_opened(), "News details page should be opened"

    news_details_page.header.change_to_en() if language == Language.EN else news_details_page.header.change_to_uk()

    news_details_page.click_edit_button()
    eco_news_id = news_details_page.get_news_id()

    edit_news_page = EditNewsPage(driver_with_login, eco_news_id)
    assert edit_news_page.is_page_opened(), "Edit News page should be opened"
    return edit_news_page


@fixture(scope="function")
def tag_selection_environment(driver_with_login):
    # Initialize the driver and navigate to Create News page
    driver = driver_with_login
    news_page = NewsPage(driver).open()
    news_page.header.change_to_en()
    create_news_page = news_page.click_create_news()
    # Yield control to the test method, passing the required Page Objects
    yield create_news_page, news_page
    # Return to the News list page to ensure a clean state
    news_page.open()
    # Reset any applied tag filters to avoid affecting subsequent tests
    news_page.remove_all_selected_tags()


@fixture(scope="session")
def get_auth_token():
    """Get auth token."""
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    assert login_response.status_code == 200, f"Fixture: Login failed with {login_response.status_code}"

    # Validate response schema to ensure required fields (including accessToken) are present
    validate_json(login_response.json(), success_sign_in_schema)

    token = login_response.json().get("accessToken")
    assert token, "Fixture: Login response does not contain 'accessToken'"
    return token

@fixture(scope="session")
def eco_news_client_with_auth_token(get_auth_token) -> EcoNewsClient:
    return EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, get_auth_token)

@fixture(scope="function")
def create_eco_news(get_auth_token, eco_news_client_with_auth_token) -> Response:
    news_payload = {
        "title": "Eco title ",
        "text": "Test content with more than 20 characters",
        "tags": [EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        "source": "https://chatgpt.com/",
        "shortInfo": "short description 12341"
    }
    response = eco_news_client_with_auth_token.add_eco_news(news_payload)
    assert 200 <= response.status_code < 300, (
        f"Fixture: Failed to create eco news, status code {response.status_code}"
    )
    news_response = response.json()
    return get_auth_token, news_response

@fixture(scope="function")
def create_delete_news_with_token(create_eco_news, eco_news_client_with_auth_token):
    with allure.step("Creating news for test and capturing its ID"):
        auth_token, news_response = create_eco_news
        news_id = news_response["id"]
    
    yield auth_token, news_response

    with allure.step(f"Cleanup: Deleting news ID {news_id}"):
        eco_news_client_with_auth_token.delete_eco_news_by_id(news_id)