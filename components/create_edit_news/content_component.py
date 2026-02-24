from components.base_component import BaseComponent
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ContentComponent(BaseComponent):
    """ Component representing the news content editor."""

    CONTENT_EDITOR = (By.CSS_SELECTOR, ".ql-editor")

    def get_editor(self) -> WebElement:
        """ Get content editor WebElement. """
        return self.find(*self.CONTENT_EDITOR)

    @allure.step("Clear content text")
    def clear_content(self):
        """ Clear text inside the content editor. """
        element = self.get_editor()
        self.clear_element_by_keyboard(element)
        return self

    @allure.step("Clear and enter content text: {text}")
    def enter_content(self, text: str):
        """ Clear editor and enter new content text. """
        element = self.get_editor()
        self.clear_element_by_keyboard(element)
        element.send_keys(text)
        return self
