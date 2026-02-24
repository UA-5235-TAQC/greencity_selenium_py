from selenium.webdriver.common.by import By
import allure
from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement


class CreateNewsPage(CreateEditNewsPage):
    """Page object for Create News page."""

    publish_btn: WebElement

    locators: LocatorsTable = {
        "publish_btn": (By.XPATH,
                        "//button[@type='submit' and contains(@class,'primary-global-button')]")
    }

    @allure.step("Click Publish button")
    def click_publish(self):
        """ Click Publish button. """
        self.publish_btn.click()
