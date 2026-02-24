from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Tuple
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
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

    def are_visible(self, locators: List[Tuple[str, str]]) -> bool:
        """ Check if all elements located by the given locators are visible. """
        try:
            self.wait_until_visible_all(locators)
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if an element located by locator is visible on the page."""
        try:
            self.wait_until_visible(locator)
            return True
        except TimeoutException:
            return False

    def wait_until_visible(self, locator: Tuple[str, str]) -> WebElement:
        """Wait until element located by locator is visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_visible_all(self, locators: List[Tuple[str, str]]) -> List[WebElement]:
        """ Wait until all elements located by the given locators are visible. """
        visible_elements = []
        for locator in locators:
            el = self.wait_until_visible(locator)
            visible_elements.append(el)
        return visible_elements

    def wait_until_invisible(self, locator: Tuple[str, str]) -> WebElement:
        """Wait until element located by locator is invisible and return it."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_until_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """ Wait until element located by locator is clickable and return it. """
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Tuple[str, str]):
        """ Click an element by locator. """
        self.wait_until_clickable(locator).click()

    def find(self, locator: Tuple[str, str]) -> WebElement:
        """ Find an element by locator. """
        return self.driver.find_element(*locator)

    def find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        """ Find all elements by locator. """
        return self.driver.find_elements(*locator)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """ Get text of the WebElement. """
        return self.wait_until_visible(locator).text.strip()

    def find_from(self, element: WebElement, locator: Tuple[str, str]) -> WebElement:
        """ Find a single element starting from a given root element. """
        return element.find_element(*locator)

    def find_all_from(self, element: WebElement, locator: Tuple[str, str]) -> List[WebElement]:
        """ Find all elements starting from a given root element. """
        return element.find_elements(*locator)

    def get_int_from_text(self, locator: Tuple[str, str], part_index: int = None) -> int:
        """ Get an integer value from the text of the element. """
        text = self.get_text(locator)
        if part_index is not None:
            text_parts = text.split(" ")
            if part_index < len(text_parts):
                text = text_parts[part_index]
            else:
                text = ""
        digits = "".join(c for c in text if c.isdigit())
        return int(digits) if digits else 0

    def clear_element_by_keyboard(self, element):
        """ Clear input element using keyboard shortcuts. """
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        return self
