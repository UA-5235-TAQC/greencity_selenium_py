from typing import List
from urllib.parse import urlparse, parse_qs

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from components.delete_news_modal import DeleteNewsModal
from components.news_details.comment_form_component import CommentFormComponent
from components.news_details.comment_item_component import CommentItemComponent
from components.news_details.news_card_component import NewsCardComponent
from data.config import Config
from pages.base_page import BasePage
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.news_page import NewsPage
from utils.page_factory import ElementNotFoundException
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
    comments_count: WebElement
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
        "comments_count": (By.CSS_SELECTOR, "#total-count"),
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
        parsed_url = urlparse(url)

        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            if "id" in query_params:
                return int(query_params["id"][0])

        if parsed_url.fragment:
            fragment = parsed_url.fragment

            if "?" in fragment:
                fragment_query = fragment.split("?", 1)[1]
                fragment_params = parse_qs(fragment_query)

                if "id" in fragment_params:
                    return int(fragment_params["id"][0])

        raise ValueError(f"Unable to extract news ID from URL: {url}")

    @allure.step("Click 'Back to news' button")
    def click_back_to_news_button(self):
        """Click the link to return to the main news list."""
        self.back_to_news_button.click()
        return NewsPage(self.driver)

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

    @allure.step("Wait until news details page is loaded")
    def wait_until_opened(self) -> "NewsDetailsPage":
        """ Wait until news details page is visible. """
        self.wait_until_visible(self.news_image)
        return self

    @allure.step("Compare news title with expected title: '{expected_title}'")
    def check_news_title(self, expected_title: str) -> bool:
        """ Compare the current news title with the expected value (case-insensitive). """
        actual = self.get_title_value()
        return actual.strip().lower() == expected_title.strip().lower()

    @allure.step("Get Edit button text")
    def get_edit_button_text(self) -> str:
        """ Return the visible text of the Edit button. """
        return self.edit_button.text.strip()

    @allure.step("Add like to the news if it is not already added")
    def add_like(self):
        """
        Add a like to the news article if it is not already liked.
        Wait until likes counter increases.
        """
        if not self.is_like_active():
            initial_count = self.get_likes_count()
            self.click_like_button()
            self.wait_for_likes_to_change(initial_count + 1)
        return self

    @allure.step("Get social icon names")
    def get_social_icon_names(self) -> List[str]:
        """ Return the list of social media icon names from the 'alt' attribute. """
        return [icon.get_attribute("alt") for icon in self.social_links]

    @allure.step("Get comments count")
    def get_comments_count(self) -> int:
        """ Return the total number of comments as integer. """
        text = self.comments_count.text.strip()
        return int(text) if text else 0

    @allure.step("Get tag by index: {index}")
    def get_tag_by_index(self, index: int) -> str:
        """ Return the tag text at the specified index. """
        if 0 <= index < len(self.tags):
            return self.tags[index].text
        raise IndexError(f"Tag with index {index} not found. Total tags: {len(self.tags)}")

    @allure.step("Check if 'Back to news' button is visible")
    def is_back_to_news_button_visible(self) -> bool:
        """ Check if the 'Back to news' button is visible. """
        return self.back_to_news_button.is_displayed()

    @allure.step("Check if 'Delete news' button is visible")
    def is_delete_button_visible(self) -> bool:
        """ Check if the Delete button is visible. """
        return self.delete_button.is_displayed()

    @allure.step("Check if Edit button is visible")
    def is_edit_button_visible(self) -> bool:
        """Check if the Edit button is visible. Return False if element does not exist."""
        try:
            return self.edit_button.is_displayed()
        except ElementNotFoundException:
            return False

    @allure.step("Check if likes count is visible")
    def is_likes_count_visible(self) -> bool:
        """ Check if the likes counter is visible. """
        return self.likes_count.is_displayed()

    @allure.step("Check if tag with name '{tag_name}' is visible")
    def is_tag_visible_by_name(self, tag_name: str) -> bool:
        """ Check whether a tag with the given name is visible. """
        return any(
            tag.text.strip().lower() == tag_name.strip().lower() and tag.is_displayed()
            for tag in self.tags
        )

    @allure.step("Check if tags are visible on page")
    def are_tags_visible(self) -> bool:
        """ Check if all tags are visible. """
        return all(tag.is_displayed() for tag in self.tags)

    @allure.step("Check if post date is visible")
    def is_post_date_visible(self) -> bool:
        """ Check if post date is visible. """
        return self.post_date.is_displayed()

    @allure.step("Check if author is visible")
    def is_author_visible(self) -> bool:
        """ Check if author name is visible. """
        return self.author_name.is_displayed()

    @allure.step("Check if content is visible")
    def is_content_visible(self) -> bool:
        """ Check if news content is visible. """
        return self.content.is_displayed()

    @allure.step("Check if news image is visible")
    def is_news_image_visible(self) -> bool:
        """ Check if the news image is visible. """
        return self.news_image.is_displayed()

    @allure.step("Check if image is present")
    def is_news_image_present(self) -> bool:
        """ Verify that the news image source exists and is a valid HTTPS link. """
        src = self.get_news_image_src()
        return src is not None and src.startswith("https://")

    @allure.step("Delete news by ID: {news_id}")
    def delete_news_by_id(self, news_id: int) -> None:
        self.open(news_id)
        if self.is_page_opened():
            modal = self.click_delete_button()
            WebDriverWait(self.driver, Config.EXPLICITLY_WAIT).until(lambda d: modal.is_component_visible())
            modal.click_yes_button()
            WebDriverWait(self.driver, Config.EXPLICITLY_WAIT).until(EC.url_contains("/news"))