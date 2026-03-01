import allure

from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from components.delete_news_modal import DeleteNewsModal
from components.news_details.comment_form_component import CommentFormComponent
from components.news_details.comment_item_component import CommentItemComponent
from components.news_details.news_card_component import NewsCardComponent
from data.config import Config
from pages.base_page import BasePage
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.news_page import NewsPage
from utils.page_factory import LocatorsTable


class NewsDetailsPage(BasePage):
    """
    Page object for the News Details page.
    Provides methods to interact with news content, likes, tags, and navigation.
    """

    back_to_news_button: WebElement
    delete_button: WebElement
    edit_button: WebElement
    like_button: WebElement
    likes_count: WebElement
    social_links: List[WebElement]
    tags: List[WebElement]
    comments: List[CommentItemComponent]
    comments_form: CommentFormComponent
    news_title_text: WebElement
    post_date: WebElement
    author_name: WebElement
    content: WebElement
    news_image: WebElement
    news_list_title: WebElement
    news_cards: List[NewsCardComponent]
    delete_news_modal: DeleteNewsModal

    locators: LocatorsTable = {
        "back_to_news_button": (By.CSS_SELECTOR, ".button-link"),
        "delete_button": (By.CSS_SELECTOR, ".secondary-global-button.delete-news-button"),
        "edit_button": (By.XPATH, "//a[div[@class='edit-news']]"),
        "like_button": (By.CSS_SELECTOR, "img.news_like"),
        "likes_count": (By.CSS_SELECTOR, ".like_wr .numerosity_likes"),
        "social_links": (By.CSS_SELECTOR, ".news-links-images img", List[WebElement]),
        "tags": (By.CSS_SELECTOR, ".tags .tags-item", List[WebElement]),
        "comments": (By.CSS_SELECTOR, ".app-comments-list", List[CommentItemComponent]),
        "comments_form": (By.CSS_SELECTOR, ".app-add-comment form", CommentFormComponent),
        "news_title_text": (By.CSS_SELECTOR, ".news-title-container .news-title"),
        "post_date": (By.CSS_SELECTOR, ".news-info-date"),
        "author_name": (By.CSS_SELECTOR, ".news-info-author"),
        "content": (By.CSS_SELECTOR, ".ql-editor"),
        "news_image": (By.CSS_SELECTOR, "img.news-image-img"),
        "news_list_title": (By.CSS_SELECTOR, ".wrapper p"),
        "news_cards": (By.CSS_SELECTOR, "app-news-list-gallery-view", List[NewsCardComponent]),
        "delete_news_modal": (By.CSS_SELECTOR, ".mdc-dialog__container", DeleteNewsModal)
    }

    @allure.step("Open news details page with ID")
    def open(self, news_id: int):
        """Open the news article page using its ID."""
        url = f"{Config.BASE_UI_GREEN_CITY_URL}/news/{news_id}"
        self.driver.get(url)
        return self

    @allure.step("Extract news ID from URL")
    def get_news_id(self) -> int:
        """Extract and return the news ID from the current URL."""
        url = self.driver.current_url
        try:
            news_id_str = url.rstrip('/').split('/')[-1]
            return int(news_id_str)
        except (IndexError, ValueError):
            raise ValueError(f"Unable to extract news ID from URL: {url}")

    @allure.step("Click 'Back to news' button")
    def click_back_to_news_button(self):
        """Click the link to return to the main news list."""
        self.back_to_news_button.click()
        return NewsPage(self.driver)

    @allure.step("Click 'Delete news' button")
    def click_delete_button(self) -> DeleteNewsModal:
        """Click the delete button and return the Modal component."""
        self.delete_button.click()
        return self.delete_news_modal

    @allure.step("Click 'Edit news' button")
    def click_edit_button(self):
        """Click the edit button and return the EditNewsPage object."""
        self.edit_button.click()
        return EditNewsPage(self.driver, self.get_news_id())

    @allure.step("Check if Edit button is enabled")
    def is_edit_button_enabled(self) -> bool:
        """Return True if the edit button is interactive."""
        return self.edit_button.is_enabled()

    @allure.step("Click 'Like' button")
    def click_like_button(self):
        """Perform a click action on the like image/button."""
        self.like_button.click()
        return self

    @allure.step("Remove like from the news if it is active")
    def delete_like(self):
        """Uncheck the like if the article is currently liked."""
        if self.is_like_active():
            initial_count = self.get_likes_count()
            self.click_like_button()
            self.wait_for_likes_to_change(initial_count - 1)
        return self

    @allure.step("Wait until likes count changes to expected value: {expected_count}")
    def wait_for_likes_to_change(self, expected_count: int):
        """Wait until the likes counter text matches the expected integer."""
        self.wait_for(lambda _: self.get_likes_count() == expected_count, timeout=5)

    @allure.step("Check if like is active on the page")
    def is_like_active(self) -> bool:
        """Check the 'src' attribute of the like button to see if it is in 'liked' state."""
        src = self.like_button.get_attribute("src")
        return src is not None and "liked.png" in src

    @allure.step("Get likes count")
    def get_likes_count(self) -> int:
        """Extract and return the number of likes as an integer."""
        text = self.likes_count.text
        return int(text.strip()) if text.strip() else 0

    @allure.step("Get news tags")
    def get_tags(self) -> List[str]:
        """Return a list of strings containing the names of all tags attached to the news."""
        return [el.text for el in self.tags]

    @allure.step("Get title text")
    def get_title_value(self) -> str:
        """Return the main headline of the news article."""
        return self.news_title_text.text.strip()

    @allure.step("Get post date")
    def get_post_date(self) -> str:
        """Return the formatted string of the publication date."""
        return self.post_date.text.strip()

    @allure.step("Get author name")
    def get_author(self) -> str:
        """Return the name of the author, stripping the 'by ' prefix."""
        text = self.author_name.text
        return text[3:].strip() if len(text) > 3 else text.strip()

    @allure.step("Get content text")
    def get_content_text(self) -> str:
        """Return the body text of the news article."""
        return self.content.text

    @allure.step("Get news image src")
    def get_news_image_src(self) -> str:
        """Return the source URL of the main news image."""
        return self.news_image.get_attribute("src")

    @allure.step("Check that News Details page is opened")
    def is_page_opened(self) -> bool:
        """ Verify that the News Details page is opened. """
        return self.news_title_text.is_displayed()

    @allure.step("Get title text of recommended news section")
    def get_title_text(self) -> str:
        """Return the header text of the recommended news section."""
        return self.news_list_title.text

    @allure.step("Get recommended card by index: {index}")
    def get_card_by_index(self, index: int) -> NewsCardComponent:
        """ Return a NewsCardComponent at the specified index. """
        cards = self.news_cards
        if 0 <= index < len(cards):
            return cards[index]
        raise IndexError(f"Card with index {index} is not found. Total cards: {len(cards)}")

    @allure.step("Delete news by ID: {news_id}")
    def delete_news_by_id(self, news_id: int) -> None:
        """Delete news by ID."""
        self.open(news_id)
        if self.is_page_opened():
            modal = self.click_delete_button()
            WebDriverWait(self.driver, 5).until(lambda d: modal.is_component_visible())
            modal.click_yes_button()
        else:
            raise IndexError(f"Card with ID {news_id} was not found.")

    @allure.step("Delete list of news by IDs: {news_ids}")
    def delete_news_list_by_ids(self, news_ids: set[int]) -> None:
        """Iterates through a set of news IDs and deletes each one."""
        for news_id in news_ids:
            self.delete_news_by_id(news_id)

    @allure.step("Check if news exists")
    def is_news_exist(self, news_id: int) -> bool:
        """Check if news exists."""
        try:
            self.open(news_id)
            return self.news_title_text.is_displayed()
        except Exception:
            return False
