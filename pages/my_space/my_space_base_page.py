from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure

from pages.base_page import BasePage


class MySpaceBasePage(BasePage):
    profile_panel_locator = (By.XPATH, "//div[@class='left-column']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Open My Space Page")
    def open(self) -> "MySpaceBasePage":
        """ Navigate to the My Space (Profile) page. """
        self.driver.get(self.get_base_host() + "/profile")
        return self

    @allure.step("Check if My Space Page is opened")
    def is_page_opened(self) -> bool:
        """ Verify that the My Space page is opened. """
        return self.is_visible(self.profile_panel_locator)
