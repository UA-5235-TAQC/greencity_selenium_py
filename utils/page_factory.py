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
    """Базовий клас для помилок PageFactory."""
    pass


class ElementNotFoundException(PageFactoryException):
    pass


class ElementNotVisibleException(PageFactoryException):
    pass


class PageFactory:
    """
    Базовий клас для всіх компонентів та сторінок.
    Забезпечує доступ до драйвера та логіку пошуку елементів відносно контексту.
    """
    driver: WebDriver
    timeout: int = 10

    # Використання глобального типу для словника локаторів
    locators: LocatorsTable = {}

    def __init__(self, context: Union[WebDriver, WebElement]):
        # Зберігаємо контекст пошуку (драйвер або елемент)
        self.root_element = context

        # Якщо передано WebElement, отримуємо драйвер через властивість .parent
        if isinstance(context, WebElement):
            self.driver = context.parent
        else:
            self.driver = context

    def __getattr__(self, name: str) -> Any:
        if name in self.locators:
            return self._get_element(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _get_element(self, name: str) -> Any:
        config = self.locators[name]
        by_type = config[0]
        selector = config[1]
        component_class = config[2] if len(config) > 2 else None

        locator = (by_type, selector)

        try:
            wait = WebDriverWait(self.root_element, self.timeout)

            wait.until(EC.presence_of_element_located(locator))
            element = wait.until(EC.visibility_of_element_located(locator))

            if component_class:
                return component_class(element)

            # Повертаємо стандартний WebElement замість проксі-класу
            return element

        except (TimeoutException, NoSuchElementException) as e:
            raise ElementNotFoundException(
                f"Елемент '{name}' не знайдено за локатором {locator} у контексті {self.__class__.__name__}"
            ) from e


__all__ = [
    "PageFactory",
    "PageFactoryException",
    "ElementNotFoundException",
    "ElementNotVisibleException",
    "LocatorStrategy",
    "LocatorsTable",
]