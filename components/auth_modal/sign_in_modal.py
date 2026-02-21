from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import override

from components.auth_modal.modal_base_page import ModalBasePage


class SignInModal(ModalBasePage):
    __password_field_locator = (By.ID, "password")
    __forgot_password_link_locator = (By.CSS_SELECTOR, "a.forgot-password")
    __show_password_icon_locator = (By.CSS_SELECTOR, ".image-show-hide-password")
    __sign_up_link_locator = (By.CSS_SELECTOR, "a.green-link")
    __password_field_error_locator = (By.CSS_SELECTOR, "#pass-err-msg div")

    def __init__(self, root: WebElement):
        super().__init__(root)

    @allure.step("Enter value in password field")
    def enter_password(self, password: str) -> SignInModal:
        self.root.find_element(*self.__password_field_locator).send_keys(password)
        return self

    @allure.step("Click show password icon")
    def click_show_password(self) -> None:
        self.root.find_element(*self.__show_password_icon_locator).click()

    @allure.step("Click forgot password link")
    def click_forgot_password(self) -> None:
        self.root.find_element(*self.__forgot_password_link_locator).click()

    @allure.step("Click sign up link")
    def click_sign_up_link(self) -> "SignUpModal":
        from components.auth_modal.sign_up_modal import SignUpModal
        self.root.find_element(*self.__sign_up_link_locator).click()
        return SignUpModal(self.root)

    @allure.step("Enter email and password values")
    def sign_in(self, *, email: str, password: str) -> None:
        self.enter_email(email) \
            .enter_password(password)

    @allure.step("Get password field value")
    def get_password_field_value(self) -> str:
        return self.root.find_element(*self.__password_field_locator).get_attribute("value")

    @allure.step("Check if password field error is displayed")
    def is_invalid_password_error_displayed(self) -> bool:
        return self._is_error_displayed(self.__password_field_error_locator)

    @override
    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        self._trigger_errors()
        status = [
            self.is_invalid_email_error_displayed(),
            self.is_invalid_password_error_displayed(),
        ]
        is_valid = all(x == False for x in status)
        return is_valid
