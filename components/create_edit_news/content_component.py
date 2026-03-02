import re

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable, ElementNotFoundException
from utils.web_element_utils import clear_element_by_keyboard


class ContentComponent(BaseComponent):
    """ Component representing the news content editor."""

    content_editor: WebElement
    content_toolbar: WebElement
    content_counter: WebElement
    content_message: WebElement

    locators: LocatorsTable = {
        "content_editor": (By.CSS_SELECTOR, ".ql-editor"),
        "content_toolbar": (By.CSS_SELECTOR, ".ql-toolbar"),
        "content_counter": (By.CSS_SELECTOR, "p.quill-counter"),
        "content_message": (By.CSS_SELECTOR, ".title-wrapper p.field-info")
    }

    @allure.step("Clear content text")
    def clear_content(self):
        """Clears all text from the rich text editor."""
        clear_element_by_keyboard(self.content_editor)
        return self

    @allure.step("Clear and enter content text: {text}")
    def enter_content(self, text: str):
        """Clears the editor and enters new content text."""
        self.clear_content()
        self.content_editor.send_keys(text)
        return self

    @allure.step("Enter content text without clearing: {text}")
    def enter_content_not_clear(self, text: str):
        """Appends text to the current content without clearing it."""
        self.content_editor.send_keys(text)
        return self

    @allure.step("Prepend text to existing content: {text_to_add}")
    def prepend_content(self, text_to_add: str):
        """Adds text to the beginning of the existing content."""
        current_value = self.get_content_text()
        new_value = text_to_add + (current_value if current_value else "")
        self.enter_content(new_value)
        return self

    @allure.step("Get content character counter text")
    def get_content_counter_text(self) -> str:
        """Returns the text from the character counter element."""
        return self.content_counter.text

    @allure.step("Check if content is invalid (highlighted in red)")
    def is_content_invalid(self) -> bool:
        """Checks if the character counter has the 'warning' CSS class."""
        class_attr = self.content_counter.get_attribute("class")
        return "warning" in class_attr if class_attr else False

    @allure.step("Check if content is valid")
    def is_content_valid(self) -> bool:
        """Checks if the character counter has the 'quill-valid' CSS class."""
        class_attr = self.content_counter.get_attribute("class")
        return "quill-valid" in class_attr if class_attr else False

    @allure.step("Check if content editor is visible")
    def is_content_visible(self) -> bool:
        """Checks if the rich text editor area is displayed."""
        return self.content_editor.is_displayed()

    @allure.step("Check if content toolbar is visible")
    def is_content_toolbar_visible(self) -> bool:
        """Checks if the editor formatting toolbar is displayed."""
        return self.content_toolbar.is_displayed()

    @allure.step("Get content text")
    def get_content_text(self) -> str:
        """Returns the current plain text from the editor."""
        return self.content_editor.text

    @allure.step("Get informational message text")
    def get_content_message(self) -> str:
        """Returns the text of the informational message/warning below the editor."""
        return self.content_message.text.strip()

    @allure.step("Get content validation message text")
    def get_content_warning_text(self) -> str:
        """Returns validation warning message text."""
        return self.content_message.text.strip()

    @allure.step("Get content warning message color")
    def get_content_warning_color(self) -> str:
        """Returns CSS color of validation message."""
        return self.content_message.value_of_css_property("color")

    @allure.step("Get content placeholder text")
    def get_content_placeholder(self) -> str:
        """Returns the placeholder text of the rich text editor."""
        return self.content_editor.get_attribute("data-placeholder").strip()

    @allure.step("Check if informational message is displayed")
    def is_content_warning_displayed(self) -> bool:
        """Checks if the informational message element is visible."""
        try:
            return self.content_message.is_displayed()
        except ElementNotFoundException:
            return False

    @allure.step("Get actual content character count")
    def get_actual_content_length(self) -> int:
        """
        Parses the counter text to determine the actual number of characters entered.
        Handles both 'X characters' and 'X characters Left' formats.
        """
        text = self.get_content_counter_text()
        match = re.search(r'\d+', text)

        if not match:
            return 0

        number = int(match.group())
        # if content length lower than 20, massage format is "Not enough characters. Left: X "
        if "Left" in text:
            return 20 - number

        return number

    def _remove_content_chars(self, count: int, from_start: bool):
        """Internal helper to remove a specific number of characters from the start or end."""
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
        """Removes the specified number of characters from the end of the text."""
        return self._remove_content_chars(count, from_start=False)

    @allure.step("Remove first {count} characters from content")
    def remove_first_content_chars(self, count: int):
        """Removes the specified number of characters from the start of the text."""
        return self._remove_content_chars(count, from_start=True)
