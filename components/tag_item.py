import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable, ElementNotFoundException


class TagItem(BaseComponent):
    """Component representing an individual tag item (e.g., in news or search filters)."""

    name_element: WebElement
    close_icon: WebElement

    locators: LocatorsTable = {
        "name_element": (By.CSS_SELECTOR, "a.global-tag .text"),
        "close_icon": (By.CSS_SELECTOR, "a.global-tag div")
    }

    def __init__(self, context):
        super().__init__(context)

    @allure.step("Get tag name")
    def get_name(self) -> str:
        """Returns the visible text name of the tag."""
        return self.name_element.text.strip()

    @allure.step("Verify if tag is selected")
    def is_selected(self) -> bool:
        """
        Checks if the tag is currently selected by verifying the presence 
        of the 'global-tag-close-icon' class on the close icon element.
        """
        try:
            classes = self.close_icon.get_attribute("class")
            return classes is not None and "global-tag-close-icon" in classes
        except ElementNotFoundException:
            return False

    @allure.step("Click on tag")
    def click(self):
        """Clicks on the tag name element to select or deselect it."""
        self.name_element.click()
        return self