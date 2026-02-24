from typing import List

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement

from utils.web_element_utils import get_int_from_text


class ToDoListComponent(BaseComponent):
    """ Component representing the To-do list section on the MySpace page. """

    to_do_list_container: WebElement
    header: WebElement
    items_count_label: WebElement
    to_do_items: List[WebElement]

    locators: LocatorsTable = {
        "to_do_list_container": (By.CSS_SELECTOR, "app-to-do-list .outer"),
        "header": (By.CSS_SELECTOR, "app-to-do-list .header"),
        "items_count_label": (By.CSS_SELECTOR, "app-to-do-list .items-count"),
        "to_do_items": (By.CSS_SELECTOR, "app-to-do-list .to-do-list-block > div:not(.header-position)")
    }

    @allure.step("Get To-do list header text")
    def get_header(self) -> str:
        """ Return the text of the to-do list header. """
        return self.header.text

    @allure.step("Get number of To-do items")
    def get_items_count(self) -> int:
        """ Return the number of to-do items displayed. """
        return get_int_from_text(self.items_count_label)

    @allure.step("Get all visible To-do items text")
    def get_to_do_items(self) -> List[str]:
        """ Return a list of texts for all visible to-do items. """
        return [item.text.strip() for item in self.to_do_items]

    @allure.step("Get text of to-do item at index {index}")
    def get_item(self, index: int) -> str:
        """ Return the text of a to-do item by index. """
        items = self.to_do_items
        if index < 0 or index >= len(items):
            raise IndexError(f"Invalid index {index}. To-do list contains {len(items)} items.")
        return items[index].text.strip()

    @allure.step("Check if To-do list component is visible")
    def is_visible(self) -> bool:
        """ Return True if the To-do list component is visible. """
        return self.to_do_list_container.is_displayed()
