from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.my_space.my_space_base_page import MySpaceBasePage

class MySpaceHabitsTabPage(MySpaceBasePage):

    _NO_DATA_COMPONENT = (By.CSS_SELECTOR, ".no-data app-no-data")
    _ADD_HABIT_BUTTON = (By.ID, "create-button-add-new-habit")

    def has_habits(self) -> bool:
        elements = self.driver.find_elements(*self._NO_DATA_COMPONENT)
        return len(elements) == 0

    def click_add_habit(self):
        self.wait.until(EC.element_to_be_clickable(self._ADD_HABIT_BUTTON)).click()
        return self