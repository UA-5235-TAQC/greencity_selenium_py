import allure

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class TagItem(BaseComponent):
    """Represents a tag item component on the EcoNews page."""

    name: WebElement
    close_icon: WebElement

    locators: LocatorsTable = {
        "name": (By.CSS_SELECTOR, "a.global-tag .text"),
        "close_icon": (By.CSS_SELECTOR, "a.global-tag div")
    }

    @allure.step("Get tag name")
    def get_name(self) -> str:
        """ Return the visible text of the tag. """
        return self.name.text.strip()

    @allure.step("Verify if tag is selected")
    def is_selected(self) -> bool:
        """Check if the tag is selected."""
        # Use root_element to avoid WebDriverWait timeouts for non-existent close_icon
        classes = self.root_element.get_attribute("class")
        return "global-tag-close-icon" in classes if classes else False

    @allure.step("Click on tag")
    def click_tag(self):
        """ Click on the tag's name element. """
        self.root_element.click()
