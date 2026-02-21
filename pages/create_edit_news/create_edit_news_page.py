from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class CreateEditNewsPage(BasePage):
    root_locator = (By.CSS_SELECTOR, "div.main-content")
    title_input_locator = (By.CSS_SELECTOR, "textarea[formcontrolname='title']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self) -> "CreateEditNewsPage":
        """Open Create/Edit News page."""
        self.driver.get(self.get_base_host() + "/news/create-news")
        return self

    def is_page_opened(self) -> bool:
        """Check if the Create/Edit News is visible."""
        return self.is_visible(self.title_input_locator)
