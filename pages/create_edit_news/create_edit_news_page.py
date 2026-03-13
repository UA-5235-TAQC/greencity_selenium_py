from typing import List

import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import override

from components.create_edit_news.cancel_modal_component import CancelModalComponent
from components.create_edit_news.content_component import ContentComponent
from components.create_edit_news.image_component import ImageComponent
from components.tag_component import TagItem
from pages.base_page import BasePage
from utils.page_factory import ElementNotFoundException, LocatorsTable
from utils.web_element_utils import enter_text, clear_element_by_keyboard


class CreateEditNewsPage(BasePage):  # pylint: disable=too-many-public-methods
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
        "cancel_modal": (By.CSS_SELECTOR, "mat-dialog-container.mdc-dialog--open",
                        CancelModalComponent)
    }

    @allure.step("Open Create News page")
    def open(self):
        """ Opens the direct URL of the create news page."""
        self.driver.get(self.get_base_host() + "/news/create-news")
        return self

    @allure.step("Check if Create/Edit News page is opened")
    def is_page_opened(self) -> bool:
        """Check if the Create/Edit News is visible."""
        try:
            return self.title_input.is_displayed()
        except ElementNotFoundException:
            return False

    @allure.step("Check if tag buttons are visible")
    def are_tags_visible(self) -> bool:
        """ Check if tag buttons are visible. """
        return all(tag.root_element.is_displayed() for tag in self.tags)

    @allure.step("Returns names of all tags")
    def get_all_tags(self) -> List[str]:
        """ Returns names of all tags. """
        return [tag.get_name() for tag in self.tags]

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

    @allure.step("Select tag: {tag_name}")
    def select_tag(self, tag_name: str):
        """ Selects a tag by its name. """
        return self.click_tag_by_name(tag_name)

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

    @allure.step("Check if source input is visible")
    def is_source_visible(self) -> bool:
        """ Check if source input is visible. """
        return self.source_input.is_displayed()

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

    @allure.step("Get source value")
    def get_source(self) -> str:
        """ Get source value. """
        return (self.source_input.get_attribute("value") or "").strip()

    @allure.step("Get source placeholder")
    def get_source_placeholder(self) -> str:
        """ Get source placeholder. """
        return (self.source_input.get_attribute("placeholder") or "").strip()

    @allure.step("Get source message text")
    def get_source_message_text(self) -> str:
        """Returns the hint or error text below the source field."""
        return self.source_message.text.strip()

    @allure.step("Clear title input")
    def clear_title_field(self):
        """ Clear title input. """
        clear_element_by_keyboard(self.title_input)
        return self

    @allure.step("Enter news title: {title}")
    def enter_title(self, title: str):
        """ Enter title into the news title input field. """
        enter_text(self.title_input, title)
        return self

    @allure.step("Get title value")
    def get_title_value(self) -> str:
        """Returns the current text entered in the title field."""
        return self.title_input.get_attribute("value")

    @allure.step("Get title length")
    def get_title_length(self) -> int:
        """Return the number of characters currently entered in the title field."""
        return len(self.get_title_value() or "")

    @allure.step("Check if title field is highlighted in red because it's empty")
    def is_title_invalid(self) -> bool:
        """Return True if title input has 'ng-invalid' class (empty/invalid field)."""
        class_attr = self.title_input.get_attribute("class") or ""
        return "ng-invalid" in class_attr

    @allure.step("Get title counter text")
    def get_title_counter_text(self) -> str:
        """ Get title counter text. """
        return self.title_character_counter.text

    @allure.step("Append text to title: {additional_text}")
    def append_title(self, additional_text: str):
        """ Append the given text to the current title input. """
        self.title_input.send_keys(additional_text)
        return self

    @allure.step("Prepend text to title: {text}")
    def prepend_title(self, text: str):
        """Prepends the specified text to the existing title."""
        current = self.get_title_value() or ""
        return enter_text(self.title_input, text + current)

    def _remove_title_chars(self, count: int, from_start: bool):
        """Remove 'count' characters from the title input."""
        current = self.get_title_value() or ""

        if len(current) <= count:
            enter_text(self.title_input, "")
            return self

        if from_start:
            enter_text(self.title_input, current[count:])
        else:
            enter_text(self.title_input, current[:-count])

        return self

    @allure.step("Remove first {count} characters from title")
    def remove_first_title_chars(self, count: int):
        """ Remove first 'count' characters from title. """
        return self._remove_title_chars(count, True)

    @allure.step("Remove last {count} characters from title")
    def remove_last_title_chars(self, count: int):
        """ Remove the last 'count' characters from the title input. """
        return self._remove_title_chars(count, False)

    @allure.step("Check if Cancel button is visible")
    def is_cancel_button_visible(self) -> bool:
        return self.cancel_btn.is_displayed()

    @allure.step("Get Cancel button text")
    def get_cancel_button_text(self) -> str:
        """ Return the visible text of the Cancel button. """
        return self.cancel_btn.text.strip()

    @allure.step("Click Cancel button")
    def click_cancel(self) -> CancelModalComponent:
        """ Click the Cancel button on the Create/Edit News page. """
        self.cancel_btn.click()
        return self.cancel_modal

    @allure.step("Check if Preview button is visible")
    def is_preview_button_visible(self) -> bool:
        """ Check if Preview button is visible. """
        return self.preview_btn.is_displayed()

    @allure.step("Get Preview button text")
    def get_preview_button_text(self) -> str:
        """ Return the visible text of the Preview button. """
        return self.preview_btn.text.strip()

    @allure.step("Click Preview button")
    def click_preview(self) -> "NewsPreviewPage":
        """ Click the Preview button to go to the news preview page. """
        self.preview_btn.click()
        from pages.create_edit_news.news_preview_page import NewsPreviewPage  # pylint: disable=import-outside-toplevel
        return NewsPreviewPage(self.driver)

    @allure.step("Get author name")
    def get_author(self) -> str:
        """ Return the author name displayed on the page. """
        return self.author_name.text.strip()

    @allure.step("Check if author is visible")
    def is_author_visible(self) -> bool:
        """ Return True if the author element is displayed, else False. """
        return self.author_name.is_displayed()

    @allure.step("Get post date")
    def get_post_date(self) -> str:
        """ Return the post date displayed on the page. """
        return self.post_date.text.strip()

    @allure.step("Check if post date is visible")
    def is_post_date_visible(self) -> bool:
        """ Return True if the post date element is visible, else False. """
        return self.post_date.is_displayed()

    @allure.step("Check if page header is visible after clicking Back from NewsPreviewPage")
    def is_page_opened_after_preview_click_back(self) -> bool:
        """ Check if page header is visible after clicking Back from NewsPreviewPage. """
        return self.page_title_header.is_displayed()

    @override
    @allure.step("Wait until Create/Edit News page is fully opened")
    def wait_until_opened(self):
        """ Wait until Create/Edit News page is fully opened. """
        self.wait_until_visible(self.post_date)
        return self

    @allure.step("Check that Title field is valid")
    def is_title_valid(self) -> bool:
        """Verify whether the Title field is valid."""
        return "ng-invalid" not in self.title_input.get_attribute("class")

    @allure.step("Click the preview button")
    def click_preview_button(self) -> "NewsPreviewPage":
        """ Click the preview button. """
        self.preview_btn.click()
        from pages.create_edit_news.news_preview_page import NewsPreviewPage  # pylint: disable=import-outside-toplevel
        return NewsPreviewPage(self.driver)
