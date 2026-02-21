from typing_extensions import override
from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure


class CreateNewsPage(CreateEditNewsPage):
    """Page object for Create News page."""
    publish_btn_locator = (
        By.XPATH,
        "//button[@type='submit' and contains(@class,'primary-global-button')]"
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def publish_btn(self) -> WebElement:
        return self.driver.find_element(*self.publish_btn_locator)

    @allure.step("Open Create News page")
    @override
    def open(self) -> "CreateNewsPage":
        super().open()
        return self
