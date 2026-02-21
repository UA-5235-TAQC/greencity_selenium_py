from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import override
import allure
from pages.my_space.my_space_base_page import MySpaceBasePage


class MySpaceHabitsTabPage(MySpaceBasePage):
    """ Page Object representing the 'Habits' tab in My Space page. """
    add_habit_button_locator = (By.ID, "create-button-add-new-habit")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @override
    @allure.step("Verify that My Space Habits tab is opened")
    def is_page_opened(self) -> bool:
        """  Check if the Habits tab is opened by verifying visibility of Add Habit button. """
        return self.is_visible(self.add_habit_button_locator)
