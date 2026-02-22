import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from components.base_component import BaseComponent


class ContentComponent(BaseComponent):
    _content_editor = (By.CSS_SELECTOR, ".ql-editor")
    _content_toolbar = (By.CSS_SELECTOR, ".ql-toolbar")
    _content_counter = (By.CSS_SELECTOR, "p.quill-counter")
    _content_message = (By.CSS_SELECTOR, ".title-wrapper p.field-info")

    def __init__(self, root, driver, timeout=None):
        super().__init__(root, driver, timeout)

    def _clear_element_by_keyboard(self, element):
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        return self

    @allure.step("Clear content text")
    def clear_content(self):
        element = self.root.find_element(*self._content_editor)
        self._clear_element_by_keyboard(element)
        return self

    @allure.step("Clear and enter content text: {text}")
    def enter_content(self, text):
        self.clear_content()
        self.root.find_element(*self._content_editor).send_keys(text)
        return self

    @allure.step("Enter content text without clearing: {text}")
    def enter_content_not_clear(self, text):
        self.root.find_element(*self._content_editor).send_keys(text)
        return self

    @allure.step("Prepend text to existing content: {text_to_add}")
    def prepend_content(self, text_to_add):
        current_value = self.get_content_text()
        new_value = text_to_add + (current_value if current_value else "")
        self.enter_content(new_value)
        return self

    @allure.step("Get content character counter text")
    def get_content_counter_text(self) -> str:
        return self.root.find_element(*self._content_counter).text

    @allure.step("Check if content is invalid (highlighted in red)")
    def is_content_invalid(self) -> bool:
        class_attr = self.root.find_element(*self._content_counter).get_attribute("class")
        return "warning" in class_attr if class_attr else False

    @allure.step("Check if content is valid")
    def is_content_valid(self) -> bool:
        class_attr = self.root.find_element(*self._content_counter).get_attribute("class")
        return "quill-valid" in class_attr if class_attr else False

    @allure.step("Check if content editor is visible")
    def is_content_visible(self) -> bool:
        return self.root.find_element(*self._content_editor).is_displayed()

    @allure.step("Check if content toolbar is visible")
    def is_content_toolbar_visible(self) -> bool:
        return self.root.find_element(*self._content_toolbar).is_displayed()

    @allure.step("Get content text")
    def get_content_text(self) -> str:
        return self.root.find_element(*self._content_editor).text

    @allure.step("Get informational message text")
    def get_content_message(self) -> str:
        return self.root.find_element(*self._content_message).text.strip()

    @allure.step("Get content placeholder text")
    def get_content_placeholder(self) -> str:
        return self.root.find_element(*self._content_editor).get_attribute("data-placeholder").strip()

    @allure.step("Check if informational message is displayed")
    def is_content_warning_displayed(self) -> bool:
        try:
            return self.root.find_element(*self._content_message).is_displayed()
        except:
            return False

    @allure.step("Get actual content character count")
    def get_actual_content_length(self) -> int:
        text = self.get_content_counter_text()
        match = re.search(r'\d+', text)

        if not match:
            return 0

        number = int(match.group())

        if "Left" in text:
            return 20 - number

        return number

    def _remove_content_chars(self, count: int, from_start: bool):
        current_value = self.get_content_text()
        if current_value:
            if from_start:
                new_value = current_value[count:] if len(current_value) > count else ""
            else:
                new_value = current_value[:-count] if len(current_value) > count else ""
            self.enter_content(new_value)
        return self

    @allure.step("Remove last {count} characters from content")
    def remove_last_content_chars(self, count: int):
        return self._remove_content_chars(count, from_start=False)

    @allure.step("Remove first {count} characters from content")
    def remove_first_content_chars(self, count: int):
        return self._remove_content_chars(count, from_start=True)
