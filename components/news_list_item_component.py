from typing import List
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable


class NewsListItemComponent(BaseComponent):
    """ Represents the news card of the EcoNews page. """

    news_image: WebElement
    bookmark_btn: WebElement
    tags: List[WebElement]
    title: WebElement
    news_text: WebElement
    creation_date: WebElement
    author_name: WebElement
    comments_count: WebElement
    likes_count: WebElement
    overlay_backdrop: WebElement

    locators: LocatorsTable = {"news_image": (By.CSS_SELECTOR, ".list-image-content"),
                               "bookmark_btn": (By.CSS_SELECTOR, ".favourite-button"),
                               "tags": (By.CSS_SELECTOR, ".filter-tag div", List[WebElement]),
                               "title": (By.CSS_SELECTOR, ".title-list"),
                               "news_text": (By.CSS_SELECTOR, ".list-text"),
                               "creation_date": (By.CSS_SELECTOR, ".text-nowrap>span"),
                               "author_name": (By.CSS_SELECTOR, ".mw"),
                               "comments_count": (By.XPATH, ".//img[contains(@alt, 'comment')]/parent::*/span"),
                               "likes_count": (By.XPATH, ".//img[contains(@alt, 'likes')]/parent::*/span"),
                               "overlay_backdrop": (By.CSS_SELECTOR, ".cdk-overlay-backdrop-showing")}

    @allure.step("Click bookmark button")
    def click_bookmark(self) -> "NewsPage":
        """ Click the bookmark button of the news item. """
        self.bookmark_btn.click()
        from pages.news_page import NewsPage  # pylint: disable=import-outside-toplevel
        return NewsPage(self.driver)

    @allure.step("Click news item")
    def click_image(self) -> "NewsDetailsPage":
        """ Click the news image to open the news details page. """
        self.news_image.click()
        from pages.news_details_page import NewsDetailsPage  # pylint: disable=import-outside-toplevel
        return NewsDetailsPage(self.driver)

    @allure.step("Get list of tag texts for this news item")
    def get_tags(self) -> List[str]:
        """ Return a list of tag names as text, cleaned from extra characters like '|'. """
        return [tag.text.replace("|", "").strip() for tag in self.tags]

    @allure.step("Verify news item has expected tags")
    def has_tags(self, tag_names: List[str]) -> bool:
        """ Verify that the news item contains expected tags. """
        t = self.timeout
        by, selector = self.locators["tags"][:2]
        WebDriverWait(self.driver, t).until(
            EC.visibility_of_all_elements_located((by, selector))
        )
        displayed_tags = self.get_tags()
        return (len(displayed_tags) == len(tag_names) and all(tag in displayed_tags for tag in tag_names))

    @allure.step("Get news title text")
    def get_title(self) -> str:
        """ Get title text of the news item. """
        return self.title.text.strip()

    @allure.step("Get news text")
    def get_news_text(self) -> str:
        """ Get news description text. """
        return self.news_text.text

    @allure.step("Get news creation date")
    def get_creation_date(self) -> str:
        """ Get creation date text. """
        return self.creation_date.text

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        """ Get author name text. """
        return self.author_name.text

    @allure.step("Get comments count")
    def get_comments_count(self) -> int:
        """ Get number of comments. """
        return int(self.comments_count.text)

    @allure.step("Get likes count")
    def get_likes_count(self) -> int:
        """ Get number of likes. """
        return int(self.likes_count.text)

    @allure.step("Get bookmark button text")
    def get_bookmark_button_text(self) -> str:
        """ Get bookmark button text. """
        return self.bookmark_btn.text

    @allure.step("Open news by clicking card")
    def open_news_by_card(self) -> "NewsDetailsPage":
        """ Open news by clicking card. """
        self.root_element.click()
        from pages.news_details_page import NewsDetailsPage  # pylint: disable=import-outside-toplevel
        return NewsDetailsPage(self.driver)
