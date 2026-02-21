from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Union
from selenium.webdriver.remote.webelement import WebElement

from data.config import Config


class Base:
    """
    Base class providing core WebDriver utilities for page objects.
    All page classes and components should inherit from this Base class.
    """
    driver: WebDriver
    wait: WebDriverWait

    def __init__(self, driver: WebDriver):
        """
        Initialize the Base class with WebDriver, WebDriverWait, ActionChains,
        and JavaScript executor.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.IMPLICITLY_WAIT)

    def are_visible(self, elements: List[WebElement]) -> bool:
        """ Check if a list of elements are visible on the page. """
        try:
            self.wait_until_visible_all(elements)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_visible(self, element: WebElement) -> bool:
        try:
            self.wait_until_visible(element)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_until_visible(self, element: WebElement):
        """ Wait until the given element is visible on the page. """
        self.wait.until(EC.visibility_of(element))

    def wait_until_visible_all(self, elements: List[WebElement]):
        """ Wait until all WebElements in the list are visible. """
        for element in elements:
            self.wait_until_visible(element)

    def wait_until_clickable(self, target: Union[WebElement, tuple]):
        """Wait until element (WebElement or locator) is clickable."""
        return self.wait.until(EC.element_to_be_clickable(target))
