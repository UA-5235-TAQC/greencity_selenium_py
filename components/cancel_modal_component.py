import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from components.base_component import BaseComponent
from pages.ubs_courier_page import UbsCourierPage


class CancelModalComponent(BaseComponent):
    _message_container = (By.CSS_SELECTOR, ".warning-text")
    _yes_cancel_btn = (By.CSS_SELECTOR, ".buttons-container .primary-global-button")
    _continue_editing_btn = (By.CSS_SELECTOR, ".buttons-container .secondary-global-button")
    _close_btn = (By.CSS_SELECTOR, ".close")
    _warning_title = (By.CSS_SELECTOR, ".warning-title")
    _warning_subtitle = (By.CSS_SELECTOR, ".warning-subtitle")

    def __init__(self, root, driver, timeout=None):
        super().__init__(root, driver, timeout)

    @allure.step("Get cancel modal message text")
    def get_message(self) -> str:
        return self.root.find_element(*self._message_container).text.strip()

    @allure.step("Click 'Yes, cancel' button in cancel modal")
    def click_yes_cancel(self):
        self.root.find_element(*self._yes_cancel_btn).click()
        return UbsCourierPage(self.driver)

    @allure.step("Click 'Continue editing' button in cancel modal")
    def click_continue_editing(self):
        self.root.find_element(*self._continue_editing_btn).click()

    @allure.step("Get 'Yes, cancel' button text")
    def get_yes_cancel_button_text(self) -> str:
        return self.root.find_element(*self._yes_cancel_btn).text.strip()

    @allure.step("Get 'Continue editing' button text")
    def get_continue_editing_button_text(self) -> str:
        return self.root.find_element(*self._continue_editing_btn).text.strip()

    @allure.step("Click close (X) button in cancel modal")
    def click_close(self):
        self.root.find_element(*self._close_btn).click()

    @allure.step("Check if cancel modal is visible")
    def is_visible(self) -> bool:
        return self.root.is_displayed()

    @allure.step("Get cancel modal warning title text")
    def get_warning_title_text(self) -> str:
        return self.root.find_element(*self._warning_title).text.strip()

    @allure.step("Get cancel modal warning subtitle text")
    def get_warning_subtitle_text(self) -> str:
        return self.root.find_element(*self._warning_subtitle).text.strip()

    @allure.step("Check if 'Yes, cancel' button is visible")
    def is_cancel_button_visible(self) -> bool:
        element = self.root.find_element(*self._yes_cancel_btn)
        return element.is_displayed()

    @allure.step("Check if 'Continue editing' button is visible")
    def is_continue_editing_button_visible(self) -> bool:
        element = self.root.find_element(*self._continue_editing_btn)
        return element.is_displayed()

    @allure.step("Wait until cancel modal becomes visible")
    def wait_until_visible(self):
        self.wait.until(EC.visibility_of(self.root))

    @allure.step("Wait until cancel modal is closed")
    def wait_until_closed(self):
        self.wait.until(EC.invisibility_of_element(self.root))
