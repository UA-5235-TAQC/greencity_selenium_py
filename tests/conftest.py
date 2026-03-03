from pytest import fixture

from components.base_page.header_component import HeaderComponent
from data.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.news_page import NewsPage


@fixture(scope="function", params=["chrome"])
def get_driver(request):
    # before test execution, initialize the driver based on the browser parameter
    browser = request.param
    headless = Config.HEADLESS_MODE

    driver = None

    match browser:
        case "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
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
    # after test execution, quit the driver
    driver.quit()


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