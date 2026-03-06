import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from components.base_component import BaseComponent
from data.config import Config
from utils.page_factory import LocatorsTable


class DeleteNewsModal(BaseComponent):
    warning_text: WebElement
    yes_btn: WebElement
    no_btn: WebElement

    locators: LocatorsTable = {"warning_text": (By.CSS_SELECTOR, ".warning-title"),
                               "yes_btn": (By.XPATH, ".//button[normalize-space()='yes']"),
                               "no_btn": (By.XPATH, ".//button[normalize-space()='no']")}

    @allure.step("Confirm deletion of news")
    def click_yes_button(self):
        """Click yes button to delete news"""
        wait = WebDriverWait(self.driver, Config.EXPLICITLY_WAIT)
        btn = self.yes_btn
        wait.until(EC.element_to_be_clickable(btn))
        btn.click()

        try:
            wait.until(EC.staleness_of(btn))
        except TimeoutException:
            pass

    @allure.step("Cancel deletion of news")
    def click_no_btn(self):
        """Click no button to cancel deletion of news"""
        self.no_btn.click()

    @allure.step("Get warning text")
    def get_warning_text(self):
        """Get delete news warning text"""
        return self.warning_text.text.strip()

    @allure.step("Check if delete news modal is visible")
    def is_component_visible(self) -> bool:
        """Check if delete news modal is visible."""
        return self.is_visible()
