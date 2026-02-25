from components.base_component import BaseComponent
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utils.page_factory import LocatorsTable
from utils.web_element_utils import clear_element_by_keyboard, enter_text


class ContentComponent(BaseComponent):
    """ Component representing the news content editor."""

    content_editor: WebElement

    locators: LocatorsTable = {
        "content_editor": (By.CSS_SELECTOR, ".ql-editor")
    }

    @allure.step("Clear content text")
    def clear_content(self):
        """ Clear text inside the content editor. """
        clear_element_by_keyboard(self.content_editor)
        return self

    @allure.step("Clear and enter content text: {text}")
    def enter_content(self, text: str):
        """ Clear editor and enter new content text. """
        enter_text(self.content_editor, text)
        return self
