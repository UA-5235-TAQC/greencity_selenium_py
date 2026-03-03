from typing import Optional, override

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable


class MySpaceHabitsTabPage(MySpaceBasePage):
    """ Page Object representing the 'My habits' tab in My Space page. """

    add_habit_button: WebElement
    image: WebElement
    title: WebElement
    description: WebElement

    locators: LocatorsTable = {
        "image": (By.CSS_SELECTOR, ".picture img"),
        "title": (By.CSS_SELECTOR, ".description__title h2"),
        "description": (By.CSS_SELECTOR, ".description__advise p"),
        "add_habit_button": (By.ID, "create-button-add-new-habit")
    }

    @override
    @allure.step("Verify that My Space Habits tab is opened")
    def is_page_opened(self) -> bool:
        """  Check if the Habits tab is opened by verifying visibility of Add Habit button. """
        self.wait_until_visible(self.image)
        return self.image.is_displayed()

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

    @allure.step("Click Add Habit button")
    def click_add_habit(self):
        """ Click Add Habit button. """
        self.add_habit_button.click()
        return self

    @allure.step("Wait until My Space Habits tab is fully opened")
    def wait_until_opened(self, timeout=10) -> "MySpaceHabitsTabPage":
        """ Wait until My Space Habits tab is fully opened. """
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.is_page_opened(),
            message=f"Page {self.__class__.__name__} after {timeout} seconds is not opened"
        )
        return self
