from typing import Any, Type, Union, Dict, Tuple, Optional

from selenium.common.exceptions import (NoSuchElementException, TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LocatorStrategy = Tuple[By, str, Optional[Type[Any]]]
LocatorsTable = Dict[str, LocatorStrategy]


class PageFactoryException(Exception):
    """Base exception for PageFactory-related errors."""
    pass


class ElementNotFoundException(PageFactoryException):
    """Raised when an element cannot be found within the specified timeout."""
    pass


class ElementNotVisibleException(PageFactoryException):
    """Raised when an element is found but not visible within the specified timeout."""
    pass


class PageFactory:
    """
    Base class for all components and pages.
    Provides access to the driver and logic for finding elements relative to the context.
    """
    driver: WebDriver
    timeout: int = 10

    locators: LocatorsTable = {}

    def __init__(self, context: Union[WebDriver, WebElement]):
        """ Initializes the PageFactory with a given context (WebDriver or WebElement). """
        self.root_element = context

        if isinstance(context, WebElement):
            self.driver = context.parent
        else:
            self.driver = context

    def __getattr__(self, name: str) -> Any:
        """ Overrides attribute access to provide lazy loading of elements defined in 'locators'. """
        if name in self.locators:
            return self._get_element(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _get_element(self, name: str) -> Any:
        """ Resolves an element based on the locator configuration defined in 'locators'. """
        config = self.locators[name]
        by_type = config[0]
        selector = config[1]
        component_class = config[2] if len(config) > 2 else None

        locator = (by_type, selector)

        wait = WebDriverWait(self.root_element, self.timeout)

        try:
            wait.until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
            raise ElementNotFoundException(
                f"Element '{name}' not found using locator {locator} in context {self.__class__.__name__}") from e

        try:
            element = wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            raise ElementNotVisibleException(
                f"Element '{name}' found using locator {locator}, but it did not become visible in context {self.__class__.__name__}"
            ) from e

        except NoSuchElementException as e:
            raise ElementNotFoundException(
                f"Element '{name}' not found using locator {locator} in context {self.__class__.__name__}"
            ) from e

        if component_class:
            return component_class(element)

        return element


__all__ = [
    "PageFactory",
    "PageFactoryException",
    "ElementNotFoundException",
    "ElementNotVisibleException",
    "LocatorStrategy",
    "LocatorsTable",
]
