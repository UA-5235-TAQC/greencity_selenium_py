import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.auth_modal.modal_base_page import ModalBasePage
from components.auth_modal.sign_in_modal import SignInModal


class ForgotPasswordModal(ModalBasePage):
    """ Component representing the "Forgot Password" modal window. """

    back_to_sign_in: WebElement

    locators = {
        "back_to_sign_in": (By.CLASS_NAME, "green-link")
    }

    @allure.step("Click back to sign in link")
    def click_back_to_sign_in(self) -> SignInModal:
        """ Click the "Back to Sign In" link. """
        self.back_to_sign_in.click()
        return SignInModal(self.auth_modal)
