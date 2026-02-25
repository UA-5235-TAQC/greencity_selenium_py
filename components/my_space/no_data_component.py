from typing import Optional

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class NoDataComponent(BaseComponent):
    """ Represents a "No Data" placeholder component. """

    NO_DATA_CONTAINER = (By.CSS_SELECTOR, ".container")
    IMAGE = (By.CSS_SELECTOR, ".picture img")
    TITLE = (By.CSS_SELECTOR, ".description__title h2")
    DESCRIPTION = (By.CSS_SELECTOR, ".description__advise p")

    @allure.step("Get 'No Data' placeholder title text")
    def get_title(self) -> str:
        """Return the title text of the placeholder."""
        return self.get_text(self.TITLE)

    @allure.step("Get 'No Data' placeholder description text")
    def get_description(self) -> str:
        """Return the description text of the placeholder."""
        return self.get_text(self.DESCRIPTION)

    @allure.step("Get 'No Data' placeholder image source URL")
    def get_image_src(self) -> Optional[str]:
        """
        Return the 'src' attribute of the image element.
        Returns None if the image element is not found.
        """
        element = self.find(self.IMAGE)
        src = element.get_attribute("src") if element else None
        return src.strip() if src else None

    @allure.step("Check if 'No Data' placeholder is visible")
    def is_displayed(self) -> bool:
        """Return True if the 'No Data' component is visible on the page."""
        return self.is_visible(self.NO_DATA_CONTAINER)
