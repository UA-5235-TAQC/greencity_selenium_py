from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BaseComponent:
    root: WebElement

    def __init__(self, root: WebElement):
        self.root = root

    def get_driver(self) -> WebDriver:
        return self.root.parent

    def is_enabled(self) -> bool:
        return self.root.is_enabled()

    def is_visible(self) -> bool:
        return self.root.is_displayed()