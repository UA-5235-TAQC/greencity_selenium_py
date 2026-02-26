from typing import List
import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable

class MySpaceHabitsTabPage(MySpaceBasePage):

    no_data_components: List[WebElement] 
    add_habit_button: WebElement

    locators: LocatorsTable = {
        "no_data_components": (By.CSS_SELECTOR, ".no-data app-no-data"),
        "add_habit_button": (By.ID, "create-button-add-new-habit"),
    }

    @allure.step("Check if user has habits")
    def has_habits(self) -> bool:
        return len(self.no_data_components) == 0

    @allure.step("Click Add Habit button")
    def click_add_habit(self):
        self.add_habit_button.click()
        return self