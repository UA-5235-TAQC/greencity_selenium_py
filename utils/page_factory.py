import logging
from typing import Any, Type, Union, Dict, Tuple, Optional, get_origin, get_args

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

LocatorStrategy = Tuple[By, str, Optional[Type[Any]]]
LocatorsTable = Dict[str, LocatorStrategy]

_STALE_RETRY_ATTEMPTS = 3


class PageFactoryException(Exception):
    """Base exception for PageFactory-related errors."""


class ElementNotFoundException(PageFactoryException):
    """Raised when an element cannot be found within the specified timeout."""


class ElementNotVisibleException(PageFactoryException):
    """Raised when an element is found but not visible within the specified timeout."""


class PageFactory:
    """
    Base class for all components and pages.
    Provides access to the driver and logic for finding elements relative to the context.
    """
    driver: WebDriver
    timeout: int = 10

    locators: LocatorsTable = {}

    def __init__(self, context: Union[WebDriver, WebElement]) -> None:
        """ Initializes the PageFactory with a given context (WebDriver or WebElement). """
        self.root_element = context

        if isinstance(context, WebElement):
            self.driver = context.parent
        else:
            self.driver = context

        all_locators: LocatorsTable = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'locators'):
                all_locators.update(cls.locators)

        self.locators = all_locators

    def __getattr__(self, name: str) -> Any:
        """ Overrides attribute access to provide lazy loading of elements defined in 'locators'. """
        if name in self.locators:
            return self._resolve(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _resolve(self, name: str) -> Any:
        """Universal resolver for single or multiple elements."""

        config = self.locators[name]
        by_type = config[0]
        selector = config[1]
        component_class: Optional[Type[Any]] = None
        multiple = False

        if len(config) > 2:
            multiple = get_origin(config[2]) is list
            component_class = config[2] if not multiple else get_args(config[2])[0]

        locator = (by_type, selector)
        for attempt in range(1, _STALE_RETRY_ATTEMPTS + 1):
            wait = WebDriverWait(self.root_element, self.timeout)
            try:
                if multiple:
                    elements = wait.until(EC.presence_of_all_elements_located(*locator))
                    visible = [el for el in elements if el.is_displayed()]

                    if not visible:
                        raise ElementNotVisibleException(
                            f"Elements '{name}' found using locator {locator}, "
                            f"but none are visible in context {self.__class__.__name__}"
                        )

                    if component_class and component_class is not WebElement:
                        return [component_class(el) for el in visible]

                    return visible

                else:
                    element = wait.until(EC.presence_of_element_located(*locator))

                    if component_class:
                        return component_class(element)

                    return element

            except StaleElementReferenceException as exc:
                if attempt == _STALE_RETRY_ATTEMPTS:
                    raise ElementNotFoundException(
                        f"Element(s) '{name}' became stale after {_STALE_RETRY_ATTEMPTS} "
                        f"retries using locator {locator} in context {self.__class__.__name__}"
                    ) from exc
                logger.debug(
                    "StaleElementReferenceException for '%s' (attempt %d/%d), retrying...",
                    name,
                    attempt,
                    _STALE_RETRY_ATTEMPTS,
                )
            except TimeoutException as exc:
                raise ElementNotFoundException(
                    f"Element(s) '{name}' not found using locator {locator} "
                    f"in context {self.__class__.__name__}"
                ) from exc

    def wait_for_element(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """Wait for a single element to be present and return it."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(EC.presence_of_element_located(*locator))

    def wait_for_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """Wait for a single element to be *visible* and return it."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(*locator))


__all__ = [
    "PageFactory",
    "PageFactoryException",
    "ElementNotFoundException",
    "ElementNotVisibleException",
    "LocatorStrategy",
    "LocatorsTable",
]
