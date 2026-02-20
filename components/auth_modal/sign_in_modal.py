from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.auth_modal.modal_base_page import ModalBasePage
from components.auth_modal.sign_up_modal import SignUpModal


class SignInModal(ModalBasePage):
    __password_field_locator = (By.ID, "password")
    __forgot_password_link_locator = (By.CSS_SELECTOR, "a.forgot-password")
    __show_password_icon_locator = (By.CSS_SELECTOR, ".image-show-hide-password")
    __sign_up_link_locator = (By.CLASS_NAME, "green-link")

    def __init__(self, root: WebElement):
        super().__init__(root)

    def enter_password(self, password: str) -> None:
        self.root.find_element(*self.__password_field_locator).send_keys(password)

    def click_show_password(self) -> None:
        self.root.find_element(*self.__show_password_icon_locator).click()

    def click_forgot_password(self) -> None:
        self.root.find_element(*self.__forgot_password_link_locator).click()

    def click_sign_up_link(self) -> SignUpModal:
        self.root.find_element(*self.__sign_up_link_locator).click()
        return SignUpModal(self.root)

    def sign_in(self, *, email: str, password: str) -> None:
        self.enter_email(email)
        self.enter_password(password)
