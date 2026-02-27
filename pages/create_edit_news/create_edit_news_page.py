from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from components.create_edit_news.cancel_modal_component import CancelModalComponent
from components.create_edit_news.content_component import ContentComponent
from components.create_edit_news.image_component import ImageComponent
from components.tag_component import TagItem
from pages.base_page import BasePage
from pages.create_edit_news.news_preview_page import NewsPreviewPage
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement

from utils.web_element_utils import enter_text, clear_element_by_keyboard


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
    page_title_header: WebElement
    source_message: WebElement
    cancel_btn: WebElement
    preview_btn: WebElement
    title_character_counter: WebElement
    post_date: WebElement
    author_name: WebElement
    cancel_modal: CancelModalComponent

    locators: LocatorsTable = {
        "title_input": (By.CSS_SELECTOR, "textarea[formcontrolname='title']"),
        "tags": (By.CSS_SELECTOR, "div.tags-box button.tag-button", List[TagItem]),
        "source_input": (By.CSS_SELECTOR, "input[formcontrolname='source']"),
        "image_component": (By.CSS_SELECTOR, "div.image-block", ImageComponent),
        "content_component": (By.CSS_SELECTOR, "div.textarea-wrapper", ContentComponent),
        "page_title_header": (By.CSS_SELECTOR, "div.title h2.title-header"),
        "source_message": (By.CSS_SELECTOR, "div.source-block"),
        "cancel_btn": (By.CSS_SELECTOR, ".submit-buttons button.tertiary-global-button"),
        "preview_btn": (By.CSS_SELECTOR, ".submit-buttons button.secondary-global-button"),
        "title_character_counter": (By.CSS_SELECTOR, ".title-block div span.field-info"),
        "post_date": (By.CSS_SELECTOR, "div.date p:nth-of-type(1) span:last-child"),
        "author_name": (By.CSS_SELECTOR, "div.date p:nth-of-type(2) span:last-child"),
        "cancel_modal": (By.CSS_SELECTOR, "mat-dialog-container app-warning-pop-up", CancelModalComponent)
    }

    @allure.step("Open Create News page")
    def open(self):
        """ Opens the direct URL of the create news page."""
        self.driver.get(self.get_base_host() + "/news/create-news")
        return self

    @allure.step("Check if Create/Edit News page is opened")
    def is_page_opened(self) -> bool:
        """Check if the Create/Edit News is visible."""
        return self.title_input.is_displayed()

    @allure.step("Enter news title: {title}")
    def enter_title(self, title: str):
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

    @allure.step("Get selected tag names")
    def get_selected_tags(self) -> list[str]:
        """Returns a list of names for all tags currently marked as selected."""
        return [tag.get_name() for tag in self.tags if tag.is_selected()]

    @allure.step("Select multiple tags: {tag_names}")
    def select_tags(self, tag_names: list[str]):
        """Selects the specified tags if they are not already selected."""
        for name in tag_names:
            target = next((t for t in self.tags if t.get_name().lower() == name.lower()), None)
            if target and not target.is_selected():
                target.click_tag()
        return self

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
    def enter_source(self, url: str):
        """ Enter source into the news source input field. """
        enter_text(self.source_input, url)
        return self

    @allure.step("Clear source field")
    def clear_source_field(self):
        """Completely removes text from the source field."""
        clear_element_by_keyboard(self.source_input)
        return self

    @allure.step("Get title value")
    def get_title_value(self) -> str:
        """Returns the current text entered in the title field."""
        return self.title_input.get_attribute("value")

    @allure.step("Get source message text")
    def get_source_message_text(self) -> str:
        """Returns the hint or error text below the source field."""
        return self.source_message.text.strip()

    @allure.step("Get cancel modal component")
    def get_cancel_modal(self) -> CancelModalComponent:
        """Returns the modal component that appears when 'Cancel' is clicked."""
        return self.cancel_modal

    @allure.step("Prepend text to title: {text}")
    def prepend_title(self, text: str):
        """Prepends the specified text to the existing title."""
        current = self.get_title_value()
        self.enter_title(text + (current if current else ""))
        return self

    @allure.step("Reload create news page")
    def reload(self):
        """Refreshes the page via the driver."""
        self.driver.refresh()
        return self

    def get_title_input(self):
        return self.title_input

    def clear_title_field(self):
        self.title_input.clear()
        return self


    def is_title_valid(self) -> bool:
        self.title_input.get_attribute("ng-invalid")

    @allure.step("Click the preview button")
    def click_preview_button(self)-> NewsPreviewPage: 
        """ Click the preview button. """
        self.preview_btn.click()
        return NewsPreviewPage(self.driver)
    