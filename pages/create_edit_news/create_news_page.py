from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage


class CreateNewsPage(CreateEditNewsPage):
    """Page object for Create News page."""
    PUBLISH_BTN = (
        By.XPATH,
        "//button[@type='submit' and contains(@class,'primary-global-button')]"
    )

    @property
    def publish_btn(self) -> WebElement:
        return self.find(*self.PUBLISH_BTN)
