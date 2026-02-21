from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import override

from components.auth_modal.modal_base_page import ModalBasePage


class SignUpModal(ModalBasePage):
    __username_field_locator = (By.ID, "firstName")
    __password_field_locator = (By.ID, "password")
    __repeat_password_field_locator = (By.ID, "repeatPassword")
    __show_password_icon_locator = (By.CSS_SELECTOR, "img.show-password-img")
    __sign_in_link_locator = (By.CLASS_NAME, "green-link")
    __password_field_error_locator = (By.CSS_SELECTOR, "p.password-not-valid")
    __confirm_password_field_error_locator = (By.ID, "confirm-err-msg")
    __username_field_error_locator = (By.ID, "firstname-err-msg")

    @allure.step("Enter value in username field")
    def enter_username(self, username: str) -> SignUpModal:
        self.root.find_element(*self.__username_field_locator).send_keys(username)
        return self

    @allure.step("Enter value in password field")
    def enter_password(self, password: str) -> SignUpModal:
        self.root.find_element(*self.__password_field_locator).send_keys(password)
        return self

    @allure.step("Enter value in confirm password field")
    def enter_confirm_password(self, password: str) -> SignUpModal:
        self.root.find_element(*self.__repeat_password_field_locator).send_keys(password)
        return self

    @allure.step("Click on show password icon")
    def show_password(self) -> None:
        self.__get_password_icon()[0].click()

    @allure.step("Click on show confirm password icon")
    def show_confirm_password(self) -> None:
        self.__get_password_icon()[1].click()

    @allure.step("Click on sign in link")
    def click_sign_in_link(self) -> "SignInModal":
        from components.auth_modal.sign_in_modal import SignInModal
        self.root.find_element(*self.__sign_in_link_locator).click()
        return SignInModal(self.root)

    @allure.step("Enter email, username, password, confirm password values")
    def sign_up(self, *, email: str, username: str, password: str, confirm_password: str) -> None:
        self.enter_email(email) \
            .enter_username(username) \
            .enter_password(password) \
            .enter_confirm_password(confirm_password)

    @allure.step("Get username field value")
    def get_username_field_value(self) -> str:
        return self.root.find_element(*self.__username_field_locator).get_attribute("value")

    @allure.step("Get password field value")
    def get_password_field_value(self) -> str:
        return self.root.find_element(*self.__password_field_locator).get_attribute("value")

    @allure.step("Get confirm password field value")
    def get_confirm_password_field_value(self) -> str:
        return self.root.find_element(*self.__repeat_password_field_locator).get_attribute("value")

    @allure.step("Check if password field error is displayed")
    def is_invalid_password_error_displayed(self) -> bool:
        return self._is_error_displayed(self.__password_field_error_locator)

    @allure.step("Check if confirm password field error is displayed")
    def is_invalid_confirm_password_error_displayed(self) -> bool:
        return self._is_error_displayed(self.__confirm_password_field_error_locator)

    @allure.step("Check if username field error is displayed")
    def is_invalid_username_error_displayed(self) -> bool:
        return self._is_error_displayed(self.__username_field_error_locator)

    @override
    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        self._trigger_errors()
        status = [
            self.is_invalid_email_error_displayed(),
            self.is_invalid_username_error_displayed(),
            self.is_invalid_password_error_displayed(),
            self.is_invalid_confirm_password_error_displayed(),
        ]
        is_valid = all(x == False for x in status)
        return is_valid

    def __get_password_icon(self) -> list[WebElement]:
        elements = self.root.find_elements(*self.__username_field_locator)
        return elements