from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent


class ModalBasePage(BaseComponent):
    """
    Base component representing an authentication modal window.
    This class provides common elements and interactions shared across
    authentication-related modals (e.g., sign-in, sign-up, password reset).
    """
    title: WebElement
    subtitle: WebElement
    submit_button: WebElement
    email_field: WebElement
    google_sign_in_button: WebElement
    close_modal_button: WebElement
    auth_modal: WebElement

    locators = {
        "title": (By.CSS_SELECTOR, "h1"), "subtitle": (By.CSS_SELECTOR, "h2"),
        "submit_button": (By.CSS_SELECTOR, "button[type='submit']"),
        "email_field": (By.ID, "email"),
        "google_sign_in_button": (By.CSS_SELECTOR, "button.google-sign-in"),
        "close_modal_button": (By.CSS_SELECTOR, ".close-modal-window"),
        "auth_modal": (By.CSS_SELECTOR, "app-auth-modal")
    }

    __email_field_error_locator = (By.CSS_SELECTOR, "#email-err-msg div")

    @allure.step("Get modal window title")
    def get_title(self) -> str:
        """ Get modal window title. """
        return self.title.text

    @allure.step("Get modal window subtitle")
    def get_subtitle(self) -> str:
        """ Get modal window subtitle. """
        return self.subtitle.text

    @allure.step("Enter value in email field")
    def enter_email(self, email: str) -> ModalBasePage:
        """ Enter value in email field. """
        self.email_field.send_keys(email)
        return self

    @allure.step("Click submit button")
    def click_submit(self) -> None:
        """ Click submit button. """
        self.submit_button.click()

    @allure.step("Click google sign in link")
    def click_google_sign_in(self) -> None:
        """ Click google sign in link. """
        self.google_sign_in_button.click()

    @allure.step("Close modal window")
    def close_modal(self) -> None:
        """ Close modal window. """
        self.close_modal_button.click()

    @allure.step("Check if submit button enabled")
    def is_submit_button_enabled(self) -> bool:
        """ Check if submit button enabled. """
        return self.submit_button.is_enabled()

    @allure.step("Get email field value")
    def get_email_field_value(self) -> str:
        """ Get email field value. """
        return self.email_field.get_attribute("value")

    @allure.step("Check if email field error is displayed")
    def is_invalid_email_error_displayed(self) -> bool:
        """ Check if email field error is displayed. """
        return self._is_error_displayed(self.__email_field_error_locator)

    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        """ Check if entered data is valid. """
        self._trigger_errors()
        return self.is_invalid_email_error_displayed()

    def _trigger_errors(self) -> None:
        """ Trigger form validation by interacting with the modal. """
        self.title.click()

    def _is_error_displayed(self, locator: tuple[str, str]) -> bool:
        """ Check whether a validation error element is displayed. """
        elements = self.root_element.find_elements(*locator)
        return len(elements) == 1 and elements[0].is_displayed()
