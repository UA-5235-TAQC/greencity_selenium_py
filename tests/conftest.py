from pytest import fixture
from data.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages.home_page import HomePage

@fixture(scope="function", params=["chrome"])
def get_driver(request):
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
    driver.quit()


@fixture(scope="function")
def logged_in_user(get_driver):
    """Returns a driver with a logged-in user"""
    home_page = HomePage(get_driver).open()
    sign_in_modal = home_page.header.click_sign_in_link()
    sign_in_modal.sign_in()
    return get_driver