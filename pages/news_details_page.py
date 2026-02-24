import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement


class NewsDetailsPage(BasePage):
    """
    Page Object representing the News Details page.
    This page displays detailed information about a specific news item,
    including title, content, author, publication date, and related actions.
    """

    news_title: WebElement

    locators: LocatorsTable = {
        "news_title": (By.CSS_SELECTOR, ".news-title-container .news-title")
    }

    def __init__(self, driver, news_id: int):
        """ Initialize the NewsDetailsPage for a specific news item. """
        super().__init__(driver)
        self.news_id = news_id

    @allure.step("Open News Details page")
    def open(self):
        """ Open the News Details page for the specified news ID. """
        self.driver.get(f"{self.get_base_host()}/news/{self.news_id}")
        return self

    @allure.step("Check that News Details page is opened")
    def is_page_opened(self) -> bool:
        """ Verify that the News Details page is opened. """
        return self.news_title.is_displayed()
