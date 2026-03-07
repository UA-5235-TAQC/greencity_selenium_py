import allure
from allure_commons.types import Severity
from data.config import Config
from pages.home_page import HomePage


@allure.epic("EcoNews UI")
@allure.feature("Main Page")
@allure.story("Page Load Verification")
@allure.title("Verify GreenCity main page loads correctly")
@allure.tag("Smoke Test")
@allure.severity(Severity.NORMAL)
def test_greencity_is_work(get_driver):
    """
    Verify that the GreenCity main page loads and
    the browser title starts with 'GreenCity'.
    """
    with allure.step("Get page title and verify"):
        title = get_driver.title
        assert title.startswith("GreenCity"), f"Expected title to start with 'GreenCity', but got '{title}'"


@allure.epic("EcoNews UI")
@allure.feature("Navigation")
@allure.story("Base Navigation Check")
@allure.title("Verify main navigation links work correctly")
@allure.tag("Smoke Test")
@allure.severity(Severity.NORMAL)
def test_base_navigate(get_driver):
    """
    Verify that the user can navigate from Home page to News page
    and back to Home page using logo.
    """
    with allure.step("Open Home page and verify title"):
        page = HomePage(get_driver).open()
        assert page.get_title().startswith("GreenCity"), "Home page title should start with 'GreenCity'"

    with allure.step("Navigate to News page via header link"):
        page = page.header.click_news_link()
        expected_news_url = f"{Config.BASE_UI_GREEN_CITY_URL}/news"
        assert page.get_current_url() == expected_news_url, \
            f"Expected URL to be {expected_news_url}, but got {page.get_current_url()}"

    with allure.step("Return to Home page via logo click"):
        page = page.header.click_logo()
        expected_home_url = Config.BASE_UI_GREEN_CITY_URL
        assert page.get_current_url() == expected_home_url, \
            f"Expected URL to be {expected_home_url}, but got {page.get_current_url()}"
