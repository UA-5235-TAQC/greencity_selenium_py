from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
import allure
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    """Concrete implementation of the Home Page."""
    root_locator = (By.CSS_SELECTOR, ".main-content")

    def __init__(self, driver: WebDriver):
        """Initialize the HomePage with all relevant sections."""
        super().__init__(driver)

    @allure.step("Open home page")
    def open(self) -> HomePage:
        """Open the HomePage URL."""
        self.driver.get(self.get_base_host())
        return self.wait_until_opened()

    @allure.step("Check that home page is opened")
    def is_page_opened(self) -> bool:
        """ Check whether the Home page is opened. """
        return self.is_visible(*self.root_locator)

    @allure.step("Wait until home page is loaded")
    def wait_until_opened(self) -> HomePage:
        """Wait until the HomePage is fully loaded."""
        self.wait.until(EC.visibility_of_element_located(self.root_locator))
        return self
