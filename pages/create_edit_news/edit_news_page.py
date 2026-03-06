from typing import List, Optional
from typing_extensions import override

import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage
from utils.page_factory import LocatorsTable


class EditNewsPage(CreateEditNewsPage):
    """ Page Object representing the Edit News page. """

    edit_btn: WebElement

    locators: LocatorsTable = {
        "edit_btn": (By.XPATH,
                     "//button[@type='submit' and contains(@class,'primary-global-button')]")
    }

    def __init__(self, driver: WebDriver, news_id: int):
        """ Initialize the Edit News page for a specific news item. """
        super().__init__(driver)
        self.news_id = news_id

    @allure.step("Open Edit News page")
    @override
    def open(self):
        """ Open the Edit News page for the specified news ID. """
        self.driver.get(
            self.get_base_host() + f"/news/create-news?id={self.news_id}"
        )
        return self

    @allure.step("Check if Edit button is visible")
    def is_edit_button_visible(self) -> bool:
        """ Check if Edit button is visible. """
        return self.edit_btn.is_displayed()

    @allure.step("Check if Edit button is enabled")
    def is_edit_button_enabled(self) -> bool:
        """ Check if Edit button is enabled. """
        return self.edit_btn.is_enabled()

    @allure.step("Click Edit button")
    def click_edit(self) -> None:
        """ Click Edit button. """
        self.edit_btn.click()

    @allure.step("Get Edit button text")
    def get_edit_button_text(self) -> str:
        """ Get Edit button text. """
        return self.edit_btn.text

    @allure.step(
        "Edit news with title: {title}, tags: {tags}, "
        "source: {source}, content: [hidden], image: {image_path}"
    )
    def edit_news(
            self,
            title: Optional[str],
            tags: Optional[List[str]],
            source: Optional[str],
            content: Optional[str],
            image_path: Optional[str],
    ):
        """ Edit news fields conditionally. """
        if title is not None:
            self.enter_title(title)

        if tags is not None:
            self.clear_all_selected_tags()
            self.select_tags(tags)

        if source is not None:
            self.enter_source(source)

        if content is not None:
            self.content_component.enter_content(content)

        if image_path is not None:
            self.image_component.change_image(image_path)

        return self

    @allure.step("Get news ID")
    def get_id(self) -> int:
        """ Get the ID of the news being edited. """
        return self.news_id

    @allure.step("Click Cancel button")
    def click_cancel(self):
        self.cancel_btn.click()
        return self

    @allure.step("Check if Edit page is opened (safe)")
    def is_page_opened_safe(self) -> bool:
        try:
            return self.title_input.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException, AttributeError):
            return False
