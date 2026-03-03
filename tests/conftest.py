from pytest import fixture
import allure

from components.news_list_item_component import NewsListItemComponent
from components.base_page.header_component import HeaderComponent
from data.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from allure_commons.types import Severity
from typing import Generator

from enums.language import Language
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.home_page import HomePage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage
from tests.utils.ui_news_test_data import NewsTestData

from pages.news_page import NewsPage


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

    sign_in_modal = (
        HomePage(get_driver)
        .open()
        .header.change_to_en()
        .click_sign_in_link()
    )

    sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    yield get_driver


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
def log_in_user(get_driver):
    header = HeaderComponent(get_driver)
    sign_in_modal = header.click_sign_in_link()
    sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)
    yield get_driver
    get_driver.delete_all_cookies()


@fixture(scope="function")
def tag_selection_environment(log_in_user):
    # Initialize the driver and navigate to Create News page
    driver = log_in_user
    news_page = NewsPage(driver).open()
    news_page.header.change_to_en()
    create_news_page = news_page.click_create_news()
    # Yield control to the test method, passing the required Page Objects
    yield create_news_page, news_page
    # Return to the News list page to ensure a clean state
    news_page.open()
    # Reset any applied tag filters to avoid affecting subsequent tests
    news_page.remove_all_selected_tags()