import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from components.tag_item import TagItem
from components.image_component import ImageComponent
from components.content_component import ContentComponent
from components.cancel_modal_component import CancelModalComponent
from pages.news_preview_page import NewsPreviewPage
from utils.page_factory import LocatorsTable


class CreateEditNewsPage(BasePage):
    """Page object class for Creating and Editing News."""

    title_input: WebElement
    page_title_header: WebElement
    source_input: WebElement
    image_root: ImageComponent
    source_message: WebElement
    cancel_btn: WebElement
    preview_btn: WebElement
    title_character_counter: WebElement
    post_date: WebElement
    author_name: WebElement
    content_root: ContentComponent
    cancel_modal: CancelModalComponent

    locators: LocatorsTable = {
        "title_input": (By.CSS_SELECTOR, "textarea[formcontrolname='title']"),
        "page_title_header": (By.CSS_SELECTOR, "div.title h2.title-header"),
        "tag_elements": (By.CSS_SELECTOR, "div.tags-box button.tag-button"),
        "source_input": (By.CSS_SELECTOR, "input[formcontrolname='source']"),
        "image_root": (By.CSS_SELECTOR, "div.image-block", ImageComponent),
        "source_message": (By.CSS_SELECTOR, "div.source-block"),
        "cancel_btn": (By.CSS_SELECTOR, ".submit-buttons button.tertiary-global-button"),
        "preview_btn": (By.CSS_SELECTOR, ".submit-buttons button.secondary-global-button"),
        "title_character_counter": (By.CSS_SELECTOR, ".title-block div span.field-info"),
        "post_date": (By.CSS_SELECTOR, "div.date p:nth-of-type(1) span:last-child"),
        "author_name": (By.CSS_SELECTOR, "div.date p:nth-of-type(2) span:last-child"),
        "content_root": (By.CSS_SELECTOR, "div.textarea-wrapper", ContentComponent),
        "cancel_modal": (By.CSS_SELECTOR, "mat-dialog-container app-warning-pop-up", CancelModalComponent)
    }

    @allure.step("Clear input element")
    def _clear_element(self, element: WebElement):
        """Internal method to fully clear an input field."""
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        return self

    @allure.step("Open Create News page")
    def open(self) -> "CreateEditNewsPage":
        """Opens the direct URL of the create news page."""
        url = f"{self.get_base_host()}/news/create-news"
        self.driver.get(url)
        return self

    @allure.step("Check if Create/Edit News page is opened")
    def is_page_opened(self) -> bool:
        """Checks the visibility of the main title input field."""
        return self.title_input.is_displayed()

    @allure.step("Enter news title: {title}")
    def enter_title(self, title: str):
        """Clears the field and enters a new news title."""
        self._clear_element(self.title_input)
        self.title_input.send_keys(title)
        return self

    @allure.step("Enter news source: {url}")
    def enter_source(self, url: str):
        """Clears the field and enters the news source URL."""
        self._clear_element(self.source_input)
        self.source_input.send_keys(url)
        return self

    @allure.step("Clear source field")
    def clear_source_field(self):
        """Completely removes text from the source field."""
        self._clear_element(self.source_input)
        return self

    @allure.step("Get all tag items")
    def get_tag_items(self) -> list[TagItem]:
        """Finds all tag elements on the page and returns them as a list of TagItem components."""
        locator = self.locators["tag_elements"][:2]
        elements = self.driver.find_elements(*locator)
        return [TagItem(el) for el in elements]

    @allure.step("Find tag by name: {tag_name}")
    def _get_tag_by_name(self, tag_name: str) -> TagItem:
        """Private method to find a TagItem object by its text name."""
        for tag in self.get_tag_items():
            if tag.get_name().lower() == tag_name.lower():
                return tag
        raise NoSuchElementException(f"Tag with name '{tag_name}' not found.")

    @allure.step("Click tag by name: {tag_name}")
    def click_tag_by_name(self, tag_name: str):
        """Finds a tag by name and performs a click on it."""
        self._get_tag_by_name(tag_name).click()
        return self

    @allure.step("Select multiple tags: {tag_names}")
    def select_tags(self, tag_names: list[str]):
        """Selects the specified tags if they are not already selected."""
        tags = self.get_tag_items()
        for name in tag_names:
            target = next((t for t in tags if t.get_name().lower() == name.lower()), None)
            if target and not target.is_selected():
                target.click()
        return self

    @allure.step("Get selected tag names")
    def get_selected_tags(self) -> list[str]:
        """Returns a list of names for all tags currently marked as selected."""
        return [tag.get_name() for tag in self.get_tag_items() if tag.is_selected()]

    @allure.step("Get title value")
    def get_title_value(self) -> str:
        """Returns the current text entered in the title field."""
        return self.title_input.get_attribute("value")

    @allure.step("Get source message text")
    def get_source_message_text(self) -> str:
        """Returns the hint or error text below the source field."""
        return self.source_message.text.strip()

    @allure.step("Click preview button")
    def click_preview(self) -> NewsPreviewPage:
        """Clicks 'Preview' and returns the news preview page object."""
        self.preview_btn.click()
        return NewsPreviewPage(self.driver)

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