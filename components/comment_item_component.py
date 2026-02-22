from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
from base_component import BaseComponent

class CommentItemComponent(BaseComponent):

    def __init__(self, driver: WebDriver, root: Optional[WebElement], timeout):
        super().__init__(root, driver, timeout)
