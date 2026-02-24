from typing import List

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class ToDoListComponent(BaseComponent):
    """ Component representing the To-do list section on the MySpace page. """

    TO_DO_LIST_CONTAINER = (By.CSS_SELECTOR, "app-to-do-list .outer")
    HEADER = (By.CSS_SELECTOR, "app-to-do-list .header")
    ITEMS_COUNT_LABEL = (By.CSS_SELECTOR, "app-to-do-list .items-count")
    TO_DO_ITEMS = (By.CSS_SELECTOR, "app-to-do-list .to-do-list-block > div:not(.header-position)")

    @allure.step("Get To-do list header text")
    def get_header(self) -> str:
        """ Return the text of the to-do list header. """
        return self.get_text(self.HEADER)

    @allure.step("Get number of To-do items")
    def get_items_count(self) -> int:
        """ Return the number of to-do items displayed. """
        return self.get_int_from_text(self.ITEMS_COUNT_LABEL)

    @allure.step("Get all visible To-do items text")
    def get_to_do_items(self) -> List[str]:
        """ Return a list of texts for all visible to-do items. """
        return self.get_texts_from(self.TO_DO_ITEMS)

    @allure.step("Get To-do item at index {index}")
    def get_item(self, index: int) -> str:
        """ Return the text of a to-do item by index. """
        texts = self.get_to_do_items()
        return self.get_text_by_index(texts, index, "to-do items")

    @allure.step("Check if To-do list component is visible")
    def is_visible(self) -> bool:
        """ Return True if the To-do list component is visible. """
        return self.is_visible(self.TO_DO_LIST_CONTAINER)
