from typing import List

from components.news_list_item_component import NewsListItemComponent
from components.tag_component import TagItem
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.remote.webelement import WebElement


class NewsPage(BasePage):
    """Page Object representing the Eco News page."""

    PAGE_TITLE = (By.CSS_SELECTOR, "h1.main-header")
    CREATE_NEWS_BUTTON = (By.CSS_SELECTOR, "div#create-button")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div:has(span.search-img)")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.place-input")
    CLOSE_SEARCH_ICON = (By.CSS_SELECTOR, "img[alt='cancel search']")
    BOOKMARK_BUTTON = (By.CSS_SELECTOR, "div:has(span.bookmark-img)")
    MY_EVENTS_BUTTON = (By.CSS_SELECTOR, "div:has(img.my-events-img)")
    GRID_VIEW_BUTTON = (By.CSS_SELECTOR, "[aria-label='table view']")
    LIST_VIEW_BUTTON = (By.CSS_SELECTOR, "[aria-label='list view']")
    REMAINING_COUNT_TEXT = (By.CSS_SELECTOR, "h2")
    NEWS_CARD_ITEMS = (By.CSS_SELECTOR, "ul.list li")
    TAG_BUTTON = (By.CSS_SELECTOR, "button.tag-button")

    @allure.step("Open Eco News page")
    def open(self):
        """Navigate to the Eco News page."""
        self.driver.get(f"{self.get_base_host()}/news")
        return self

    @allure.step("Verify Eco News page is opened")
    def is_page_opened(self) -> bool:
        """Return True if Eco News page title is visible."""
        return self.is_visible(self.PAGE_TITLE)

    @allure.step("Wait until Eco News page is opened")
    def wait_until_opened(self):
        """Wait until Eco News page title becomes visible."""
        self.wait_until_visible(self.PAGE_TITLE)
        return self

    @allure.step("Get Eco News page title")
    def get_page_title(self) -> str:
        """Return Eco News page title text."""
        return self.get_text(self.PAGE_TITLE)

    @allure.step("Get Eco News search input")
    def get_search_input(self) -> WebElement:
        """Return Eco News search input."""
        return self.find(self.SEARCH_INPUT)

    @allure.step("Enter search text: {text}")
    def enter_search(self, text: str):
        """Enter text into the search field."""
        if not self.is_visible(self.SEARCH_INPUT):
            self.click(self.SEARCH_BUTTON)
        self.get_search_input().send_keys(text)

    @allure.step("Close search input")
    def close_search(self):
        """Close search field if visible."""
        if self.is_visible(self.SEARCH_INPUT):
            self.click(self.CLOSE_SEARCH_ICON)

    @allure.step("Click Bookmark button")
    def click_bookmark(self):
        """ Click the Bookmark filter button. """
        self.click(self.BOOKMARK_BUTTON)

    @allure.step("Click My Events tab button")
    def click_my_events(self):
        """ Click the My Events page tab button. """
        self.click(self.MY_EVENTS_BUTTON)

    @allure.step("Switch news list view to grid")
    def switch_to_grid_view(self):
        """ Switch the news list display to grid view. """
        self.click(self.GRID_VIEW_BUTTON)

    @allure.step("Switch news list view to list")
    def switch_to_list_view(self):
        """ Switch the news list display to list view. """
        self.click(self.LIST_VIEW_BUTTON)

    @allure.step("Get count of remaining news")
    def get_remaining_news_count(self) -> int:
        """
        Return the number of remaining news items as an integer.
        Returns 0 if no digits are found in the remaining count text.
        """
        return self.get_int_from_text(self.REMAINING_COUNT_TEXT)

    @allure.step("Click on Create News button")
    def click_create_news(self) -> "CreateNewsPage":
        """ Click the 'Create News' button and return the CreateNewsPage instance. """
        self.click(self.CREATE_NEWS_BUTTON)
        from pages.create_edit_news.create_news_page import CreateNewsPage
        return CreateNewsPage(self.driver)

    @allure.step("Get all available tags")
    def get_all_tags(self) -> List[TagItem]:
        """ Return a list of all TagItem components present on the page. """
        tag_elements = self.find_all(self.TAG_BUTTON)
        return [TagItem(self.driver, el) for el in tag_elements]

    @allure.step("Remove all selected tags")
    def remove_all_selected_tags(self):
        """ Click all tags that are currently selected to remove their selection. """
        all_tags = self.get_all_tags()
        for tag in all_tags:
            if tag.is_selected():
                tag.click_tag()

    @allure.step("Get all news cards")
    def get_news_cards(self) -> List[NewsListItemComponent]:
        """ Return a list of all NewsListItemComponent on the page. """
        return [
            NewsListItemComponent(self.driver, el)
            for el in self.find_all(self.NEWS_CARD_ITEMS)
        ]

    @allure.step("Get a news card by index: {index}")
    def get_news_card_by_index(self, index: int) -> NewsListItemComponent:
        """ Get a news card by its index. """
        cards = self.get_news_cards()
        if index < 0 or index >= len(cards):
            raise IndexError(
                f"Invalid news card index: {index}. "
                f"Valid range: 0..{len(cards) - 1} (total cards: {len(cards)})"
            )
        return cards[index]
