from typing import Tuple, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from base import Base
import allure


class BaseComponent(Base):
    """ Base class for page components. """
    root: WebElement

    def __init__(self, driver: WebDriver, root: WebElement):
        """ Initialize the component with WebDriver and root element. """
        super().__init__(driver)
        self.root = root

    @allure.step("Get the WebDriver instance associated with this component")
    def get_driver(self) -> WebDriver:
        """ Return the WebDriver instance associated with this component. """
        return self.root.parent

    @allure.step("Check if the component is enabled")
    def is_enabled(self) -> bool:
        """Check if the component is enabled."""
        return self.root.is_enabled()

    @allure.step("Check if the component is visible")
    def is_component_visible(self) -> bool:
        """Check if the component is visible."""
        return self.root.is_displayed()

    def get_texts_from(self, locator: Tuple[str, str]) -> List[str]:
        """ Get all non-empty, stripped texts from elements found inside the component root. """
        return [
            el.text.strip()
            for el in self.find_all_from(self.root, locator)
            if el.text.strip()
        ]

    def get_text_by_index(self, texts: List[str], index: int, name: str) -> str:
        """ Get an element by index from a list of texts with index validation. """
        if index < 0 or index >= len(texts):
            raise IndexError(f"Invalid index {index} for {name}. Number of items: {len(texts)}")
        return texts[index]
