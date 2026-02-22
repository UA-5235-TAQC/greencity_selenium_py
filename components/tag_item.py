from selenium.webdriver.common.by import By
import allure

from components.base_component import BaseComponent


class TagItem(BaseComponent):
    _name = (By.CSS_SELECTOR, "a.global-tag .text")
    _close_icon = (By.CSS_SELECTOR, "a.global-tag div")

    def __init__(self, driver, root):
        self.driver = driver
        self.root = root


    @allure.step("Get tag name")
    def get_name(self):
        return self.root.find_element(*self._name).text

    @allure.step("Verify if tag is selected")
    def is_selected(self):
        classes = self.root.find_elements(*self._close_icon).get_attribute("class")
        return classes is not None and "global-tag-close-icon" in classes

    @allure.step("Click on tag")
    def click(self):
        self.root.find_element(*self._name).click()
