from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent


class NewsCardComponent(BaseComponent):
    """Component representing a single news item in the gallery."""

    image: WebElement
    title: WebElement
    content: WebElement
    tags: List[WebElement]
    date: WebElement
    author: WebElement
    comments_count: WebElement
    likes_count: WebElement

    locators = {"image": (By.CSS_SELECTOR, ".list-image-content"), "title": (By.CSS_SELECTOR, ".title-list h3"),
        "content": (By.CSS_SELECTOR, ".list-text div"),
        "tags": (By.CSS_SELECTOR, ".filter-tag .ul-eco-buttons span", List[WebElement]),
        "date": (By.CSS_SELECTOR, ".user-data-text-date:first-child span"),
        "author": (By.CSS_SELECTOR, ".user-data-text-date:nth-child(2) span.mw"),
        "comments_count": (By.CSS_SELECTOR, ".user-data-like:nth-child(1) .numerosity"),
        "likes_count": (By.CSS_SELECTOR, ".user-data-like:nth-child(2) .numerosity"), }

    @allure.step("Get news title")
    def get_title(self) -> str:
        """ Get news title. """
        return self.title.text

    @allure.step("Get news content")
    def get_content(self) -> str:
        """ Get news content. """
        return self.content.text

    @allure.step("Get news tags")
    def get_tags(self) -> List[str]:
        """ Get news tags. """
        return [tag.text for tag in self.tags]

    @allure.step("Get author name")
    def get_author(self) -> str:
        """ Get author name. """
        return self.author.text

    @allure.step("Get creation date")
    def get_date(self) -> str:
        """ Get creation date. """
        return self.date.text

    @allure.step("Get number of comments")
    def get_comments_count(self) -> int:
        """ Get number of comments. """
        return int(self.comments_count.text)

    @allure.step("Get number of likes")
    def get_likes_count(self) -> int:
        """ Get number of likes. """
        return int(self.likes_count.text)
