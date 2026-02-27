from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import override

from components.auth_modal.modal_base_page import ModalBasePage
from data.config import Config


class SignInModal(ModalBasePage):
    """ Component representing the Sign In modal window. """

    password_field: WebElement
    forgot_password_link: WebElement
    show_password_icon: WebElement
    sign_up_link: WebElement

    locators = {
        "password_field": (By.ID, "password"),
        "forgot_password_link": (By.CSS_SELECTOR, "a.forgot-password"),
        "show_password_icon": (By.CSS_SELECTOR, ".image-show-hide-password"),
        "sign_up_link": (By.CSS_SELECTOR, "a.green-link"),
    }

    __password_field_error_locator = (By.CSS_SELECTOR, "#pass-err-msg div")

    @allure.step("Enter value in password field")
    def enter_password(self, password: str) -> SignInModal:
        """ Enter value in password field. """
        self.password_field.send_keys(password)
        return self

    @allure.step("Click show password icon")
    def click_show_password(self) -> None:
        """ Click show password icon. """
        self.show_password_icon.click()

    @allure.step("Click forgot password link")
    def click_forgot_password(self) -> None:
        """ Click forgot password link. """
        self.forgot_password_link.click()

    @allure.step("Click sign up link")
    def click_sign_up_link(self) -> "SignUpModal":
        """ Click sign up link. """
        from components.auth_modal.sign_up_modal import SignUpModal
        self.sign_up_link.click()
        return SignUpModal(self.auth_modal)

    @allure.step("Enter email and password values")
    def sign_in(self) -> None:
        self.enter_email(Config.USER_EMAIL)
        self.enter_password(Config.USER_PASSWORD)
        self.click_submit()

        from pages.my_space.my_space_habits_tab_page import MySpaceHabitsTabPage
        habits_page = MySpaceHabitsTabPage(self.driver)
        habits_page.wait_until_opened()

    @allure.step("Get password field value")
    def get_password_field_value(self) -> str:
        """ Get password field value. """
        return self.password_field.get_attribute("value")

    @allure.step("Check if password field error is displayed")
    def is_invalid_password_error_displayed(self) -> bool:
        """ Check if password field error is displayed. """
        return self._is_error_displayed(self.__password_field_error_locator)

    @override
    @allure.step("Check if entered data is valid")
    def is_form_valid(self) -> bool:
        """ Check if entered data is valid. """
        self._trigger_errors()
        status = [self.is_invalid_email_error_displayed(), self.is_invalid_password_error_displayed(), ]
        is_valid = all(x == False for x in status)
        return is_valid
