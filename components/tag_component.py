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
        return self.name.text

    @allure.step("Verify if tag is selected")
    def is_selected(self) -> bool:
        """Check if the tag is selected."""
        classes = self.close_icon.get_attribute("class")
        return classes is not None and "global-tag-close-icon" in classes

    @allure.step("Click on tag")
    def click_tag(self):
        """ Click on the tag's name element. """
        self.name.click()
