from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from components.create_edit_news.content_component import ContentComponent
from components.create_edit_news.image_component import ImageComponent
from components.tag_component import TagItem
from pages.base_page import BasePage
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement

from utils.web_element_utils import enter_text


class CreateEditNewsPage(BasePage):
    """
    Page Object representing Create/Edit News page.
    Provides functionality for creating and editing news items.
    """

    title_input: WebElement
    tags: List[TagItem]
    source_input: WebElement
    image_component: ImageComponent
    content_component: ContentComponent

    locators: LocatorsTable = {
        "title_input": (By.CSS_SELECTOR, "textarea[formcontrolname='title']"),
        "tags": (By.CSS_SELECTOR, "div.tags-box button.tag-button"),
        "source_input": (By.CSS_SELECTOR, "input[formcontrolname='source']"),
        "image_component": (By.CSS_SELECTOR, "div.image-block"),
        "content_component": (By.CSS_SELECTOR, "div.textarea-wrapper")
    }

    @allure.step("Open Create News page")
    def open(self):
        """Open Create/Edit News page."""
        self.driver.get(self.get_base_host() + "/news/create-news")
        return self

    @allure.step("Check if Create/Edit News page is opened")
    def is_page_opened(self) -> bool:
        """Check if the Create/Edit News is visible."""
        return self.title_input.is_displayed()

    @allure.step("Enter news title: {title}")
    def enter_title(self, title):
        """ Enter title into the news title input field. """
        enter_text(self.title_input, title)
        return self

    def _get_tag_by_name(self, tag_name: str) -> TagItem:
        """ Find tag by its name (case-insensitive). """
        for tag in self.tags:
            if tag.get_name().lower() == tag_name.lower():
                return tag
        raise NoSuchElementException(f"Tag not found: {tag_name}")

    @allure.step("Click tag by name: {tag_name}")
    def click_tag_by_name(self, tag_name: str):
        """ Click a tag by its name. """
        self._get_tag_by_name(tag_name).click_tag()
        return self

    @allure.step("Select multiple tags: {tag_names}")
    def select_tags(self, tag_names: List[str]):
        """ Select multiple tags by their names. """
        for tag_name in tag_names:
            tag = self._get_tag_by_name(tag_name)
            if not tag.is_selected():
                tag.click_tag()
        return self

    @allure.step("Get list of selected tags")
    def get_selected_tags(self) -> List[str]:
        """ Get names of all currently selected tags. """
        return [
            tag.get_name()
            for tag in self.tags
            if tag.is_selected()
        ]

    @allure.step("Unselect tag: {tag_name}")
    def unselect_tag(self, tag_name: str):
        """ Unselect a tag by its name. """
        tag = self._get_tag_by_name(tag_name)
        if tag.is_selected():
            tag.click_tag()
        return self

    @allure.step("Clear all selected tags")
    def clear_all_selected_tags(self):
        """ Clear all selected tags. """
        for tag_name in self.get_selected_tags():
            self.unselect_tag(tag_name)
        return self

    @allure.step("Enter news source: {url}")
    def enter_source(self, url):
        """ Enter source into the news source input field. """
        enter_text(self.source_input, url)
        return self
