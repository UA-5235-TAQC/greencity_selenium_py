from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from base import Base

class BaseComponent(Base):
    root: WebElement

    def __init__(self, root: WebElement, driver: WebDriver, timeout):
        super().__init__(driver, timeout)
        self.root = root

    def get_driver(self) -> WebDriver:
        return self.root.parent

    def is_enabled(self) -> bool:
        return self.root.is_enabled()

    def is_visible(self) -> bool:
        return self.root.is_displayed()