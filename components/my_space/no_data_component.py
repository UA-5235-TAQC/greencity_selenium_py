from typing import Optional

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement


class NoDataComponent(BaseComponent):
    """ Represents a "No Data" placeholder component. """

    container: WebElement
    image: WebElement
    title: WebElement
    description: WebElement

    locators: LocatorsTable = {
        "container": (By.CSS_SELECTOR, ".container"),
        "image": (By.CSS_SELECTOR, ".picture img"),
        "title": (By.CSS_SELECTOR, ".description__title h2"),
        "description": (By.CSS_SELECTOR, ".description__advise p")
    }

    @allure.step("Get 'No Data' placeholder title text")
    def get_title(self) -> str:
        """Return the title text of the placeholder."""
        return self.title.text

    @allure.step("Get 'No Data' placeholder description text")
    def get_description(self) -> str:
        """Return the description text of the placeholder."""
        return self.description.text

    @allure.step("Get 'No Data' placeholder image source URL")
    def get_image_src(self) -> Optional[str]:
        """
        Return the 'src' attribute of the image element.
        Returns None if the image element is not found.
        """
        src = self.image.get_attribute("src") if self.image else None
        return src.strip() if src else None

    @allure.step("Check if 'No Data' placeholder is visible")
    def is_displayed(self) -> bool:
        """Return True if the 'No Data' component is visible on the page."""
        return self.container.is_displayed()
