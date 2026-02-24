from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import allure
from components.base_component import BaseComponent


class NewsListItemComponent(BaseComponent):
    """ Represents the news card of the EcoNews page. """
    NEWS_IMAGE = (By.CSS_SELECTOR, ".list-image-content")
    BOOKMARK_BTN = (By.CSS_SELECTOR, ".favourite-button")
    TAGS = (By.CSS_SELECTOR, ".filter-tag div")
    TITLE = (By.CSS_SELECTOR, ".title-list")
    NEWS_TEXT = (By.CSS_SELECTOR, ".list-text")
    CREATION_DATE = (By.CSS_SELECTOR, ".text-nowrap>span")
    AUTHOR_NAME = (By.CSS_SELECTOR, ".mw")
    COMMENTS_COUNT = (By.XPATH, ".//img[contains(@alt, 'comment')]/parent::*/span")
    LIKES_COUNT = (By.XPATH, ".//img[contains(@alt, 'likes')]/parent::*/span")
    OVERLAY_BACKDROP = (By.CSS_SELECTOR, ".cdk-overlay-backdrop-showing")

    def __init__(self, driver, root_element: WebElement):
        super().__init__(driver, root_element)
        self.news_id: int = 0

    @allure.step("Click bookmark button")
    def click_bookmark(self) -> "NewsPage":
        """ Click the bookmark button of the news item. """
        self.click(self.BOOKMARK_BTN)
        from pages.news_page import NewsPage
        return NewsPage(self.driver)

    @allure.step("Click news item")
    def click(self) -> "NewsDetailsPage":
        """ Click the news image to open the news details page. """
        self.wait_until_visible(self.OVERLAY_BACKDROP)
        self.click(self.NEWS_IMAGE)
        from pages.news_details_page import NewsDetailsPage
        return NewsDetailsPage(self.driver, self.news_id)

    @allure.step("Get news image element")
    def get_image_element(self) -> WebElement:
        """ Get the image element of the news item. """
        return self.find(self.NEWS_IMAGE)

    @allure.step("Get bookmark button element")
    def get_bookmark_button(self) -> WebElement:
        """ Get the bookmark button element. """
        return self.find(self.BOOKMARK_BTN)

    @allure.step("Get tags list")
    def get_tags_list(self) -> List[WebElement]:
        """ Get list of tag elements. """
        return self.find_all(self.TAGS)

    @allure.step("Verify news item has expected tags")
    def has_tags(self, tag_names: List[str]) -> bool:
        """ Verify that the news item contains expected tags. """
        displayed_tags = [
            tag.text.replace("|", "").strip()
            for tag in self.get_tags_list()
        ]

        expected_tags = [tag.upper() for tag in tag_names]

        return (
                len(displayed_tags) == len(expected_tags)
                and all(tag in displayed_tags for tag in expected_tags)
        )

    @allure.step("Get news title element")
    def get_title_element(self) -> WebElement:
        """ Get title element of the news item. """
        return self.find(self.TITLE)

    @allure.step("Get news title text")
    def get_title(self) -> str:
        """ Get title text of the news item. """
        return self.get_title_element().text

    @allure.step("Get news text element")
    def get_news_text_element(self) -> WebElement:
        """ Get news text element. """
        return self.find(self.NEWS_TEXT)

    @allure.step("Get news text")
    def get_news_text(self) -> str:
        """ Get news description text. """
        return self.get_news_text_element().text

    @allure.step("Get news creation date element")
    def get_creation_date_element(self) -> WebElement:
        """ Get creation date element. """
        return self.find(self.CREATION_DATE)

    @allure.step("Get news creation date")
    def get_creation_date(self) -> str:
        """ Get creation date text. """
        return self.get_creation_date_element().text

    @allure.step("Get author name element")
    def get_author_name_element(self) -> WebElement:
        """ Get author name element. """
        return self.find(self.AUTHOR_NAME)

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        """ Get author name text. """
        return self.get_author_name_element().text

    @allure.step("Get comments count element")
    def get_comments_count_element(self) -> WebElement:
        """ Get comments count element. """
        return self.find(self.COMMENTS_COUNT)

    @allure.step("Get comments count")
    def get_comments_count(self) -> int:
        """ Get number of comments. """
        return int(self.get_comments_count_element().text)

    @allure.step("Get likes count element")
    def get_likes_count_element(self) -> WebElement:
        """ Get likes count element. """
        return self.find(self.LIKES_COUNT)

    @allure.step("Get likes count")
    def get_likes_count(self) -> int:
        """ Get number of likes. """
        return int(self.get_likes_count_element().text)

    @allure.step("Get news ID")
    def get_news_id(self) -> int:
        """ Get news ID. """
        return self.news_id

    @allure.step("Get bookmark button element")
    def get_bookmark_button_element(self) -> WebElement:
        """ Get bookmark button WebElement. """
        return self.find(self.BOOKMARK_BTN)

    @allure.step("Get bookmark button text")
    def get_bookmark_button_text(self) -> str:
        """ Get bookmark button text. """
        return self.get_bookmark_button_element().text
