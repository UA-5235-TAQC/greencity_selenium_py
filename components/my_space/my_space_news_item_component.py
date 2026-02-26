from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable


class MySpaceNewsItemComponent(BaseComponent):
    """ Component representing the profile news card on the MySpace page. """

    news_container: WebElement
    image: WebElement
    title: WebElement
    tags: List[WebElement]
    creation_date: WebElement
    creation_date_icon: WebElement
    author_name: WebElement
    author_icon: WebElement

    locators: LocatorsTable = {
        "news_container": (By.CSS_SELECTOR, "div.news"),
        "image": (By.CSS_SELECTOR, ".news-image"),
        "title": (By.CSS_SELECTOR, ".news-content .title h3"),
        "tags": (By.CSS_SELECTOR, ".news-content .tags .tag-btn", List[WebElement]),
        "creation_date": (By.CSS_SELECTOR, ".user-info-date p"),
        "creation_date_icon": (By.CSS_SELECTOR, ".user-info-date img"),
        "author_name": (By.CSS_SELECTOR, ".user-info-icon p"),
        "author_icon": (By.CSS_SELECTOR, ".user-info-icon img")
    }

    def __init__(self, root_element: WebElement, news_id: int):
        """ Initialize the My Space News Item component for the specified news ID. """
        super().__init__(root_element)
        self.news_id = news_id

    @allure.step("Get news id")
    def get_id(self) -> int:
        """Returns the WebElement of the news image"""
        return self.news_id

    @allure.step("Get image element")
    def get_image_element(self) -> WebElement:
        """Returns the WebElement of the news image"""
        return self.image_element

    @allure.step("Get image src")
    def get_image_src(self) -> str:
        """Gets the source URL of the news image."""
        return self.image_element.get_attribute("src")

    @allure.step("Get tag elements")
    def get_tag_elements(self) -> List[WebElement]:
        """ Get tag elements. """
        return self.tags

    @allure.step("Get tags text")
    def get_tags(self) -> List[str]:
        """Returns a list of WebElements for the tags associated with the news"""
        return [
            tag.text.strip()
            for tag in self.get_tag_elements()
        ]

    @allure.step("Get title element")
    def get_title_element(self) -> WebElement:
        """Returns the WebElement of the news title"""
        return self.title_element

    @allure.step("Get elements title ")
    def get_title(self) -> str:
        """Gets the news title text."""
        return self.title_element.text.strip()

    @allure.step("Get creation date element")
    def get_creation_date_element(self) -> WebElement:
        """Returns the WebElement containing the creation date"""
        return self.creation_date_element

    @allure.step("Get creation date")
    def get_creation_date(self) -> str:
        """Gets the displayed creation date text"""
        return self.creation_date_element.text.strip()

    @allure.step("Get author name element")
    def get_author_name_element(self) -> WebElement:
        """Returns the WebElement containing the author's name"""
        return self.author_name_element

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        """Gets the text content of the author's name"""
        return self.author_name_element.text.strip()

    @allure.step("Check if card is visible")
    def is_displayed(self) -> bool:
        """ Return True if the cards is visible. """
        return self.news_container.is_displayed()
