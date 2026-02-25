import allure
from selenium.webdriver.remote.webelement import WebElement

from utils.page_factory import LocatorsTable, By
from components.base_component import BaseComponent


class CancelModalComponent(BaseComponent):

    # ---------- elements ----------

    message_container: WebElement
    yes_cancel_btn: WebElement
    continue_editing_btn: WebElement
    close_btn: WebElement
    warning_title: WebElement
    warning_subtitle: WebElement
    root: WebElement

    locators: LocatorsTable = {
        "message_container": (By.CSS_SELECTOR, ".warning-text"),
        "yes_cancel_btn": (By.CSS_SELECTOR, ".buttons-container .primary-global-button"),
        "continue_editing_btn": (By.CSS_SELECTOR, ".buttons-container .secondary-global-button"),
        "close_btn": (By.CSS_SELECTOR, ".close"),
        "warning_title": (By.CSS_SELECTOR, ".warning-title"),
        "warning_subtitle": (By.CSS_SELECTOR, ".warning-subtitle"),
        "root": (By.CSS_SELECTOR, ".ubs-body, .warning-modal, body"),  # fallback root
    }

    # ---------- state ----------

    @allure.step("Check cancel modal is visible")
    def is_visible(self) -> bool:
        return self.warning_title.is_displayed()

    @allure.step("Wait until cancel modal is visible")
    def wait_until_visible(self):
        _ = self.warning_title
        return self

    # ---------- getters ----------

    @allure.step("Get modal message")
    def get_message(self) -> str:
        return self.message_container.text.strip()

    @allure.step("Get warning title text")
    def get_warning_title_text(self) -> str:
        return self.warning_title.text.strip()

    @allure.step("Get warning subtitle text")
    def get_warning_subtitle_text(self) -> str:
        return self.warning_subtitle.text.strip()

    @allure.step("Get Yes Cancel button text")
    def get_yes_cancel_button_text(self) -> str:
        return self.yes_cancel_btn.text.strip()

    @allure.step("Get Continue Editing button text")
    def get_continue_editing_button_text(self) -> str:
        return self.continue_editing_btn.text.strip()

    # ---------- actions ----------

    @allure.step("Click Yes Cancel button")
    def click_yes_cancel(self):
        from pages.ubs_courier_page import UbsCourierPage
        self.yes_cancel_btn.click()
        return UbsCourierPage(self.driver)

    @allure.step("Click Continue Editing button")
    def click_continue_editing(self):
        self.continue_editing_btn.click()
        return self

    @allure.step("Click Close button")
    def click_close(self):
        self.close_btn.click()
        return self

    # ---------- state checks ----------

    @allure.step("Check Yes Cancel button visible")
    def is_cancel_button_visible(self) -> bool:
        return self.yes_cancel_btn.is_displayed()

    @allure.step("Check Continue Editing button visible")
    def is_continue_editing_button_visible(self) -> bool:
        return self.continue_editing_btn.is_displayed()