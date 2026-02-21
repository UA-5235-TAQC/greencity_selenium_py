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
