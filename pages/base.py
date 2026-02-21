from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class Base:
    driver: WebDriver
    wait: WebDriverWait

    def __init__(self, driver: WebDriver, timeout):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
