from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.auth_modal.modal_base_page import ModalBasePage
from components.auth_modal.sign_in_modal import SignInModal


class SignUpModal(ModalBasePage):
    __username_field_locator = (By.ID, "firstName")
    __password_field_locator = (By.ID, "password")
    __repeat_password_field_locator = (By.ID, "repeatPassword")
    __show_password_icon_locator = (By.CSS_SELECTOR, "img.show-password-img")
    __sign_in_link_locator = (By.CLASS_NAME, "green-link")

    def enter_username(self, username: str) -> None:
        self.root.find_element(*self.__username_field_locator).send_keys(username)

    def enter_password(self, password: str) -> None:
        self.root.find_element(*self.__password_field_locator).send_keys(password)

    def enter_confirm_password(self, password: str) -> None:
        self.root.find_element(*self.__repeat_password_field_locator).send_keys(password)

    def show_password(self) -> None:
        self.__get_password_icon()[0].click()

    def show_confirm_password(self) -> None:
        self.__get_password_icon()[1].click()

    def __get_password_icon(self) -> list[WebElement]:
        elements = self.root.find_elements(*self.__username_field_locator)
        return elements

    def click_sign_in_link(self) -> SignInModal:
        self.root.find_element(*self.__sign_in_link_locator).click()
        return SignInModal(self.root)

    def sign_up(self, *, email: str, username: str, password: str) -> None:
        self.enter_email(email)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
