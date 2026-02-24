from __future__ import annotations
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class HomePage(BasePage):
    """Concrete implementation of the Home Page."""
    ROOT = (By.CSS_SELECTOR, ".main-content")

    @allure.step("Open home page")
    def open(self) -> HomePage:
        """Open the HomePage URL."""
        self.driver.get(self.get_base_host())
        return self.wait_until_opened()

    @allure.step("Check that home page is opened")
    def is_page_opened(self) -> bool:
        """ Check whether the Home page is opened. """
        return self.is_visible(*self.ROOT)

    @allure.step("Wait until home page is loaded")
    def wait_until_opened(self):
        """Wait until the HomePage is fully loaded."""
        self.wait_until_visible(self.ROOT)
        return self
