from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import override

from components.auth_modal.modal_base_page import ModalBasePage


class SignUpModal(ModalBasePage):
    """ Component representing the Sign Up modal window. """

    username_field: WebElement
    password_field: WebElement
    repeat_password_field: WebElement
    show_password_icon: WebElement
    sign_in_link: WebElement

    locators = {"username_field": (By.ID, "firstName"), "password_field": (By.ID, "password"),
                "repeat_password_field": (By.ID, "repeatPassword"),
                "show_password_icon": (By.CSS_SELECTOR, "img.show-password-img"),
                "sign_in_link": (By.CLASS_NAME, "green-link"), }

    __password_field_error_locator = (By.CSS_SELECTOR, "p.password-not-valid")
    __confirm_password_field_error_locator = (By.ID, "confirm-err-msg")
    __username_field_error_locator = (By.ID, "firstname-err-msg")

    @allure.step("Enter value in username field")
    def enter_username(self, username: str) -> SignUpModal:
        """ Enter value in username field. """
        self.username_field.send_keys(username)
        return self

    @allure.step("Enter value in password field")
    def enter_password(self, password: str) -> SignUpModal:
        """ Enter value in password field. """
        self.password_field.send_keys(password)
        return self

    @allure.step("Enter value in confirm password field")
    def enter_confirm_password(self, password: str) -> SignUpModal:
        """ Enter value in confirm password field. """
        self.repeat_password_field.send_keys(password)
        return self

    @allure.step("Click on show password icon")
    def show_password(self) -> None:
        """ Click on show password icon. """
        self.__get_password_icon()[0].click()

    @allure.step("Click on show confirm password icon")
    def show_confirm_password(self) -> None:
        """ Click on show confirm password icon. """
        self.__get_password_icon()[1].click()

    @allure.step("Click on sign in link")
    def click_sign_in_link(self) -> "SignInModal":
        """ Click on sign in link. """
        from components.auth_modal.sign_in_modal import SignInModal  # pylint: disable=import-outside-toplevel
        self.sign_in_link.click()
        return SignInModal(self.auth_modal)

    @allure.step("Enter email, username, password, confirm password values")
    def sign_up(self, *, email: str, username: str, password: str, confirm_password: str) -> None:
        """ Enter email, username, password, confirm password values. """
        self.enter_email(email).enter_username(username).enter_password(password).enter_confirm_password(
            confirm_password)

    @allure.step("Get username field value")
    def get_username_field_value(self) -> str:
        """ Get username field value. """
        return self.username_field.get_attribute("value")

    @allure.step("Get password field value")
    def get_password_field_value(self) -> str:
        """ Get password field value. """
        return self.password_field.get_attribute("value")

    @allure.step("Get confirm password field value")
    def get_confirm_password_field_value(self) -> str:
        """ Get confirm password field value. """
        return self.repeat_password_field.get_attribute("value")

    @allure.step("Check if password field error is displayed")
    def is_invalid_password_error_displayed(self) -> bool:
        """ Check if password field error is displayed. """
        return self._is_error_displayed(self.__password_field_error_locator)

    @allure.step("Check if confirm password field error is displayed")
    def is_invalid_confirm_password_error_displayed(self) -> bool:
        """ Check if confirm password field error is displayed. """
        return self._is_error_displayed(self.__confirm_password_field_error_locator)

    @allure.step("Check if username field error is displayed")
    def is_invalid_username_error_displayed(self) -> bool:
        """ Check if username field error is displayed. """
        return self._is_error_displayed(self.__username_field_error_locator)

    @override
    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        """ Check if entered data is valid. """
        self._trigger_errors()
        status = [self.is_invalid_email_error_displayed(), self.is_invalid_username_error_displayed(),
                  self.is_invalid_password_error_displayed(), self.is_invalid_confirm_password_error_displayed(), ]
        is_valid = all(not x for x in status)
        return is_valid

    def __get_password_icon(self) -> list[WebElement]:
        """ Retrieve the password visibility toggle icons. """
        elements = self.root_element.find_elements(*self.locators["show_password_icon"])
        return elements
