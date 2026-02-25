from pages.base_page import BasePage
from data.config import Config
import allure
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from components.news_details_content_component import NewsDetailsContentComponent
from pages.edit_news_page import EditNewsPage
from pages.news_page import NewsPage
from utils.page_factory import (LocatorsTable, By)

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
    comments_container: WebElement
    comments_form: WebElement
    recommended_news_container: NewsDetailsContentComponent
    news_title_text: WebElement
    post_date: WebElement
    author_name: WebElement
    content: WebElement
    news_image: WebElement

    locators: LocatorsTable = {
        "back_to_news_button": (By.CSS_SELECTOR, ".button-link"),
        "delete_button": (By.CSS_SELECTOR, ".secondary-global-button.delete-news-button"),
        "edit_button": (By.XPATH, "//a[div[@class='edit-news']]"),
        "like_button": (By.CSS_SELECTOR, "img.news_like"),
        "likes_count": (By.CSS_SELECTOR, ".like_wr .numerosity_likes"),
        "social_links": (By.CSS_SELECTOR, ".news-links-images img"),
        "tags": (By.CSS_SELECTOR, ".tags .tags-item"),
        "comments_container": (By.XPATH, "(//app-comments-container)[1]"),
        "comments_form": (By.CSS_SELECTOR, ".app-add-comment form"),
        "recommended_news_container": (By.CSS_SELECTOR, "app-eco-news-widget", NewsDetailsContentComponent),
        "news_title_text": (By.CSS_SELECTOR, ".news-title-container .news-title"),
        "post_date": (By.CSS_SELECTOR, ".news-info-date"),
        "author_name": (By.CSS_SELECTOR, ".news-info-author"),
        "content": (By.CSS_SELECTOR, ".ql-editor"),
        "news_image": (By.CSS_SELECTOR, "img.news-image-img"),
    }

    def __init__(self, driver, news_id: int):
        """
        Initialize the News Details Page.
        
        Args:
            driver: WebDriver instance.
            news_id: Unique identifier for the news article.
        """
        super().__init__(driver)
        self.news_id = news_id

    @allure.step("Open news details page with ID")
    def open(self):
        """Open the news article page using its ID."""
        url = f"{Config.BASE_UI_GREEN_CITY_URL}/news/{self.news_id}"
        self.driver.get(url)
        return self
    
    @allure.step("Click 'Back to news' button")
    def click_back_to_news_button(self):
        """Click the link to return to the main news list."""
        self.back_to_news_button.click()
        return NewsPage(self.driver)

    @allure.step("Click 'Delete news' button")
    def click_delete_button(self):
        """Click the delete button for the current news."""
        self.delete_button.click()
        return self

    @allure.step("Click 'Edit news' button")
    def click_edit_button(self):
        """Click the edit button and return the EditNewsPage object."""
        self.edit_button.click()
        return EditNewsPage(self.driver)
    
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
        elements = self.driver.find_elements(*self.locators["tags"][:2])
        return [el.text for el in elements]

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

    @allure.step("Get news ID")
    def get_id(self) -> int:
        """Return the ID of the current news article."""
        return self.news_id

    @allure.step("Get content text")
    def get_content_text(self) -> str:
        """Return the body text of the news article."""
        return self.content.text

    @allure.step("Get news image src")
    def get_news_image_src(self) -> str:
        """Return the source URL of the main news image."""
        return self.news_image.get_attribute("src")
