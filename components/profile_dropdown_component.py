import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable


class ProfileDropdownComponent(BaseComponent):
    """Component representing the user profile dropdown menu."""

    locators: LocatorsTable = {
        "link_elements": (By.CSS_SELECTOR, "a")
    }

    def __init__(self, context):
        super().__init__(context)

    def _get_link_elements(self) -> list[WebElement]:
        """Internal helper to find all link elements within the dropdown context."""
        locator = self.locators["link_elements"][:2]
        return self.root_element.find_elements(*locator)

    @allure.step("Open notifications")
    def open_notifications(self):
        """Clicks the first link in the dropdown, which corresponds to Notifications."""
        links = self._get_link_elements()
        if links:
            links[0].click()
        return self

    @allure.step("Open personal account page")
    def open_personal_account(self):
        """Clicks the second link in the dropdown to navigate to the Personal Account."""
        links = self._get_link_elements()
        if len(links) > 1:
            links[1].click()
        return self

    @allure.step("Click Sign Out")
    def sign_out(self):
        """Clicks the last link in the dropdown to log the user out."""
        links = self._get_link_elements()
        if links:
            links[-1].click()
        return self