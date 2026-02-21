from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent


class ModalBasePage(BaseComponent):
    __title_locator = (By.CSS_SELECTOR, "h1")
    __subtitle_locator = (By.CSS_SELECTOR, "h2")
    __submit_button_locator = (By.CSS_SELECTOR, "button[type='submit']")
    __email_field_locator = (By.ID, "email")
    __google_sign_in_button_locator = (By.CSS_SELECTOR, "button.google-sign-in")
    __close_modal_button_locator = (By.CSS_SELECTOR, ".close-modal-window")
    __email_field_error_locator = (By.CSS_SELECTOR, "#email-err-msg div")

    def __init__(self, root: WebElement):
        super().__init__(root)
        self.root = root

    @allure.step("Get modal window title")
    def get_title(self) -> str:
        return self.root.find_element(*self.__title_locator).text

    @allure.step("Get modal window subtitle")
    def get_subtitle(self) -> str:
        return self.root.find_element(*self.__subtitle_locator).text

    @allure.step("Enter value in email field")
    def enter_email(self, email: str) -> ModalBasePage:
        self.root.find_element(*self.__email_field_locator).send_keys(email)
        return self

    @allure.step("Click submit button")
    def click_submit(self) -> None:
        self.root.find_element(*self.__submit_button_locator).click()

    @allure.step("Click google sign in link")
    def click_google_sign_in(self) -> None:
        self.root.find_element(*self.__google_sign_in_button_locator).click()

    @allure.step("Close modal window")
    def close_modal(self) -> None:
        self.root.find_element(*self.__close_modal_button_locator).click()

    @allure.step("Check if submit button enabled")
    def is_submit_button_enabled(self) -> bool:
        return self.root.find_element(*self.__submit_button_locator).is_enabled()

    @allure.step("Get email field value")
    def get_email_field_value(self) -> str:
        return self.root.find_element(*self.__email_field_locator).get_attribute("value")

    @allure.step("Check if email field error is displayed")
    def is_invalid_email_error_displayed(self) -> bool:
        return self._is_error_displayed(self.__email_field_error_locator)

    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        self._trigger_errors()
        return self.is_invalid_email_error_displayed()

    def _trigger_errors(self) -> None:
        self.root.find_element(*self.__title_locator).click()

    def _is_error_displayed(self, locator: tuple[str, str]) -> bool:
        elements = self.root.find_elements(*locator)
        return len(elements) == 1 and elements[0].is_displayed()