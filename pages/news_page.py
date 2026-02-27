from typing import List
from components.news_list_item_component import NewsListItemComponent
from components.tag_component import TagItem
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.remote.webelement import WebElement
from utils.page_factory import LocatorsTable
from utils.web_element_utils import get_int_from_text


class NewsPage(BasePage):
    """Page Object representing the Eco News page."""

    page_title: WebElement
    create_news_btn: WebElement
    search_btn: WebElement
    search_input: WebElement
    close_search_icon: WebElement
    bookmark_btn: WebElement
    my_events_btn: WebElement
    grid_view_btn: WebElement
    list_view_btn: WebElement
    remaining_count_text: WebElement
    news_card_items: List[NewsListItemComponent]
    tags: List[TagItem]

    locators: LocatorsTable = {
        "page_title": (By.CSS_SELECTOR, "h1.main-header"),
        "create_news_btn": (By.CSS_SELECTOR, "div#create-button"),
        "search_btn": (By.CSS_SELECTOR, "div:has(span.search-img)"),
        "search_input": (By.CSS_SELECTOR, "input.place-input"),
        "close_search_icon": (By.CSS_SELECTOR, "img[alt='cancel search']"),
        "bookmark_btn": (By.CSS_SELECTOR, "div:has(span.bookmark-img)"),
        "my_events_btn": (By.CSS_SELECTOR, "div:has(img.my-events-img)"),
        "grid_view_btn": (By.CSS_SELECTOR, "[aria-label='table view']"),
        "list_view_btn": (By.CSS_SELECTOR, "[aria-label='list view']"),
        "remaining_count_text": (By.CSS_SELECTOR, "h2"),
        "news_card_items": (By.CSS_SELECTOR, "ul.list li", List[NewsListItemComponent]),
        "tags": (By.CSS_SELECTOR, "button.tag-button", List[TagItem]),
    }

    @allure.step("Open Eco News page")
    def open(self):
        """Navigate to the Eco News page."""
        self.driver.get(f"{self.get_base_host()}/news")
        return self

    @allure.step("Verify Eco News page is opened")
    def is_page_opened(self) -> bool:
        """Return True if Eco News page title is visible."""
        return self.page_title.is_displayed()

    @allure.step("Get Eco News page title")
    def get_page_title(self) -> str:
        """Return Eco News page title text."""
        return self.page_title.text

    @allure.step("Enter search text: {text}")
    def enter_search(self, text: str):
        """Enter text into the search field."""
        if not self.search_input.is_displayed():
            self.search_btn.click()
        self.search_input.send_keys(text)

    @allure.step("Close search input")
    def close_search(self):
        """Close search field if visible."""
        if self.search_input.is_displayed():
            self.close_search_icon.click()

    @allure.step("Click Bookmark button")
    def click_bookmark(self):
        """ Click the Bookmark filter button. """
        self.bookmark_btn.click()

    @allure.step("Click My Events tab button")
    def click_my_events(self):
        """ Click the My Events page tab button. """
        self.my_events_btn.click()

    @allure.step("Switch news list view to grid")
    def switch_to_grid_view(self):
        """ Switch the news list display to grid view. """
        self.grid_view_btn.click()

    @allure.step("Switch news list view to list")
    def switch_to_list_view(self):
        """ Switch the news list display to list view. """
        self.list_view_btn.click()

    @allure.step("Get count of remaining news")
    def get_remaining_news_count(self) -> int:
        """
        Return the number of remaining news items as an integer.
        Returns 0 if no digits are found in the remaining count text.
        """
        return get_int_from_text(self.remaining_count_text)

    @allure.step("Click on Create News button")
    def click_create_news(self) -> "CreateNewsPage":
        """ Click the 'Create News' button and return the CreateNewsPage instance. """
        self.create_news_btn.click()
        from pages.create_edit_news.create_news_page import CreateNewsPage
        return CreateNewsPage(self.driver)

    @allure.step("Remove all selected tags")
    def remove_all_selected_tags(self):
        self.wait_until_opened()
        selected_tags = [tag for tag in self.tags if tag.is_selected()]
        if not selected_tags:
            return
        for tag in selected_tags:
            tag.click_tag()

    @allure.step("Get a news card by index: {index}")
    def get_news_card_by_index(self, index: int) -> NewsListItemComponent:
        """ Get a news card by its index. """
        cards = self.news_card_items
        if index < 0 or index >= len(cards):
            raise IndexError(
                f"Invalid news card index: {index}. "
                f"Valid range: 0..{len(cards) - 1} (total cards: {len(cards)})"
            )
        return cards[index]

    @allure.step("Wait until Eco News page is opened")
    def wait_until_opened(self):
        """Wait until Eco News page title becomes visible."""
        self.wait_until_visible(self.page_title)
        return self

    @allure.step("Click on tag by name: {tag_name}")
    def click_tag_by_name(self, tag_name: str):
        """ Click a tag by its visible name (case-insensitive). """
        for tag in self.get_all_tags():
            if tag.get_name().strip().lower() == tag_name.strip().lower():
                tag.click_tag()
                return self

        raise ValueError(f"Tag not found: {tag_name}")
