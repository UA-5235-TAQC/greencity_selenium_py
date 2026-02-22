from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from data.config import Config

class Base:
    driver: WebDriver
    wait: WebDriverWait

    def __init__(self, driver: WebDriver, timeout=Config.IMPLICITLY_WAIT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
