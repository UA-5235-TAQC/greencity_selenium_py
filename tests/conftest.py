from pytest import fixture

from components.auth_modal.sign_in_modal import SignInModal
from components.base_page.header_component import HeaderComponent
from data.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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
    sign_in_modal.sign_in()

    yield get_driver

    get_driver.delete_all_cookies()