from selenium.webdriver.common.by import By
from typing import override
import allure
from selenium.webdriver.support.wait import WebDriverWait

from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable, ElementNotFoundException
from selenium.webdriver.remote.webelement import WebElement


class MySpaceHabitsTabPage(MySpaceBasePage):
    """ Page Object representing the 'Habits' tab in My Space page. """


    add_habit_btn: WebElement

    locators: LocatorsTable = {
        "add_habit_btn": (By.ID, "create-button-add-new-habit")
    }

    @override
    @allure.step("Verify that My Space Habits tab is opened")
    def is_page_opened(self) -> bool:
        """ Ckeck if My Space Habits tab is opened. """
        try:
            return self.add_habit_btn.is_displayed()
        except ElementNotFoundException:
            return False

    @allure.step("Wait until My Space Habits tab is fully opened")
    def wait_until_opened(self, timeout=10) -> "MySpaceHabitsTabPage":
        """ Wait until My Space Habits tab is fully opened. """
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.is_page_opened(),
            message=f"Page {self.__class__.__name__} after {timeout} seconds is not opened"
        )
        return self