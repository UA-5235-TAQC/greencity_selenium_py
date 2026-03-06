from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable


class CommentItemComponent(BaseComponent):
    """Component representing a single comment item."""

    author_name: WebElement
    comment_text: WebElement
    comment_date: WebElement
    like_amount: WebElement
    edit_btn: WebElement
    delete_btn: WebElement
    reply_btn: WebElement
    comment_images: List[WebElement]

    locators: LocatorsTable = {"author_name": (By.CSS_SELECTOR, ".author-name"),
        "comment_text": (By.CSS_SELECTOR, ".comment-text"), "comment_date": (By.CSS_SELECTOR, ".comment-date-month"),
        "like_amount": (By.CSS_SELECTOR, ".like-amount"), "edit_btn": (By.CSS_SELECTOR, "button.edit"),
        "delete_btn": (By.CSS_SELECTOR, "button.delete"), "reply_btn": (By.CSS_SELECTOR, "button.reply"),
        "comment_images": (By.CSS_SELECTOR, ".comment-image", List[WebElement]), }

    @allure.step("Get author name")
    def get_author(self) -> str:
        """ Get author name. """
        return self.author_name.text.strip()

    @allure.step("Get comment text")
    def get_text(self) -> str:
        """ Get comment text. """
        return self.comment_text.text.strip()

    @allure.step("Get comment date")
    def get_date(self) -> str:
        """ Get comment date. """
        return self.comment_date.text

    @allure.step("Get number of likes")
    def get_like_count(self) -> int:
        """ Get number of likes. """
        return int(self.like_amount.text)

    @allure.step("Get comment images count")
    def get_images_count(self) -> int:
        """ Get comment images count. """
        return len(self.comment_images)

    @allure.step("Click Edit button")
    def click_edit(self) -> None:
        """ Click Edit button. """
        self.edit_btn.click()

    @allure.step("Click Delete button")
    def click_delete(self) -> None:
        """ Click Delete button. """
        self.delete_btn.click()

    @allure.step("Click Reply button")
    def click_reply(self) -> None:
        """ Click Reply button. """
        self.reply_btn.click()
