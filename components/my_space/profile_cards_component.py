from typing import List

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement


class ProfileCardsComponent(BaseComponent):
    """
    Component representing the profile cards section on the MySpace page.
    Each card displays information such as "Fact of the Day" and may include a title, description, and decorative image.
    """

    image: WebElement
    title: WebElement
    tags: List[WebElement]
    creation_date: WebElement
    creation_date_icon: WebElement
    author_name: WebElement
    author_icon: WebElement

    locators: LocatorsTable = {
        "image": (By.CSS_SELECTOR, ".news-image"),
        "title": (By.CSS_SELECTOR, ".news-content .title h3"),
        "tags": (By.CSS_SELECTOR, ".news-content .tags .tag-btn"),
        "creation_date": (By.CSS_SELECTOR, ".user-info-date p"),
        "creation_date_icon": (By.CSS_SELECTOR, ".user-info-date img"),
        "author_name": (By.CSS_SELECTOR, ".user-info-icon p"),
        "author_icon": (By.CSS_SELECTOR, ".user-info-icon img")
    }

    def __init__(self, driver):
        """ Initialize the news card of the MySpace page. """
        super().__init__(driver)
        self.news_id: int = 0

    @allure.step("Get card title")
    def get_title(self) -> str:
        """Return card title."""
        return self.title.text

    @allure.step("Get card title")
    def get_title(self) -> str:
        """Return card title."""
        return self.title.text

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        """ Get author name text. """
        return self.author_name.text

    @allure.step("Get news creation date")
    def get_creation_date(self) -> str:
        """ Get creation date text. """
        return self.creation_date.text

    @allure.step("Check if card is visible")
    def is_displayed(self) -> bool:
        """ Return True if the cards is visible. """
        return self.title.is_displayed()

    @allure.step("Get news ID")
    def get_news_id(self) -> int:
        """ Get news ID. """
        return self.news_id
