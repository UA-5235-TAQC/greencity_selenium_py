from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent


class ModalBasePage(BaseComponent):
    _title_locator = (By.CSS_SELECTOR, "h1")
    _subtitle_locator = (By.CSS_SELECTOR, "h2")
    _submit_button_locator = (By.CSS_SELECTOR, "button[type='submit']")
    _email_field_locator = (By.ID, "email")
    _google_sign_in_button_locator = (By.CSS_SELECTOR, "button.google-sign-in")
    _close_modal_button_locator = (By.CSS_SELECTOR, ".close-modal-window")

    def __init__(self, root: WebElement):
        super().__init__(root)
        self.root = root

    def get_title(self) -> str:
        return self.root.find_element(*self._title_locator).text

    def get_subtitle(self) -> str:
        return self.root.find_element(*self._subtitle_locator).text

    def enter_email(self, email: str) -> None:
        self.root.find_element(*self._email_field_locator).send_keys(email)

    def click_submit(self) -> None:
        self.root.find_element(*self._submit_button_locator).click()

    def click_google_sign_in(self) -> None:
        self.root.find_element(*self._google_sign_in_button_locator).click()

    def close_modal(self) -> None:
        self.root.find_element(*self._close_modal_button_locator).click()

    def is_submit_button_enabled(self) -> bool:
        return self.root.find_element(*self._submit_button_locator).is_enabled()