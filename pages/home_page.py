from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
import allure

from utils.page_factory import LocatorsTable


class HomePage(BasePage):
    """Concrete implementation of the Home Page."""
    root: WebElement
    locators: LocatorsTable = {
        "root": (By.CSS_SELECTOR, ".main-content")
    }


    @allure.step("Open home page")
    def open(self) -> HomePage:
        """Open the HomePage URL."""
        self.driver.get(self.get_base_host())
        self.root.is_displayed()
        return self

