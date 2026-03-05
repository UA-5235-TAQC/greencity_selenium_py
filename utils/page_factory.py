from typing import Any, Type, Union, Dict, Tuple, Optional, get_origin, get_args

from selenium.common.exceptions import TimeoutException
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


class ElementNotFoundException(PageFactoryException):
    """Raised when an element cannot be found within the specified timeout."""


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
            return self._resolve(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _resolve(self, name: str, multiple: bool = False) -> Any:
        """Universal resolver for single or multiple elements."""

        config = self.locators[name]
        by_type = config[0]
        selector = config[1]
        multiple = False
        component_class = None

        if len(config) > 2:
            multiple = get_origin(config[2]) is list
            component_class = config[2] if not multiple else get_args(config[2])[0]

        locator = (by_type, selector)
        wait = WebDriverWait(self.root_element, self.timeout)

        try:
            if multiple:
                elements = wait.until(
                    EC.presence_of_all_elements_located(locator)
                )
                elements = [el for el in elements if el.is_displayed()]

                if not elements:
                    raise ElementNotVisibleException(
                        f"Elements '{name}' found using locator {locator}, "
                        f"but none are visible in context {self.__class__.__name__}"
                    )

                if component_class and component_class is not WebElement:
                    return [component_class(el) for el in elements]

                return elements

            else:
                element = wait.until(
                    EC.presence_of_element_located(locator)
                )

                if component_class:
                    return component_class(element)

                return element

        except TimeoutException as e:
            raise ElementNotFoundException(
                f"Element(s) '{name}' not found using locator {locator} "
                f"in context {self.__class__.__name__}"
            ) from e



__all__ = [
    "PageFactory",
    "PageFactoryException",
    "ElementNotFoundException",
    "ElementNotVisibleException",
    "LocatorStrategy",
    "LocatorsTable",
]
