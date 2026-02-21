from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple
from selenium.webdriver.remote.webelement import WebElement

class Base:
    driver: WebDriver
    wait: WebDriverWait

    def __init__(self, driver: WebDriver, timeout):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        """ Check if a single element is visible on the page. """
        try:
            self.wait_until_visible(locator)
            return True
        except TimeoutException:
            return False

    def wait_until_visible(self, locator: Tuple[str, str]) -> WebElement:
        """Wait until element located by locator is visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))