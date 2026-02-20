from selenium.webdriver.common.by import By

from components.auth_modal.modal_base_page import ModalBasePage
from components.auth_modal.sign_in_modal import SignInModal


class ForgotPasswordModal(ModalBasePage):
    __back_to_sign_in_locator = (By.CLASS_NAME, "green-link")

    def click_back_to_sign_in(self) -> SignInModal:
        self.root.find_element(*self.__back_to_sign_in_locator).click()
        return SignInModal(self.root)