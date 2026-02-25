import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from pages.ubs_courier_page import UbsCourierPage

class CancelModalComponent(BaseComponent):
    """Component representing the confirmation modal when canceling news creation or editing."""

    message_container: WebElement
    yes_cancel_btn: WebElement
    continue_editing_btn: WebElement
    close_btn: WebElement
    warning_title: WebElement
    warning_subtitle: WebElement

    locators: LocatorsTable = {
        "message_container": (By.CSS_SELECTOR, ".warning-text"),
        "yes_cancel_btn": (By.CSS_SELECTOR, ".buttons-container .primary-global-button"),
        "continue_editing_btn": (By.CSS_SELECTOR, ".buttons-container .secondary-global-button"),
        "close_btn": (By.CSS_SELECTOR, ".close"),
        "warning_title": (By.CSS_SELECTOR, ".warning-title"),
        "warning_subtitle": (By.CSS_SELECTOR, ".warning-subtitle")
    }

    def __init__(self, context):
        super().__init__(context)

    @allure.step("Get cancel modal message text")
    def get_message(self) -> str:
        """Returns the text content of the warning message."""
        return self.message_container.text.strip()

    @allure.step("Click 'Yes, cancel' button in cancel modal")
    def click_yes_cancel(self):
        """Clicks the confirmation button to cancel the current action."""
        self.yes_cancel_btn.click()
        return UbsCourierPage(self.driver)

    @allure.step("Click 'Continue editing' button in cancel modal")
    def click_continue_editing(self):
        """Clicks the button to dismiss the modal and stay on the page."""
        self.continue_editing_btn.click()
        return self

    @allure.step("Get 'Yes, cancel' button text")
    def get_yes_cancel_button_text(self) -> str:
        """Returns the text displayed on the cancel confirmation button."""
        return self.yes_cancel_btn.text.strip()

    @allure.step("Get 'Continue editing' button text")
    def get_continue_editing_button_text(self) -> str:
        """Returns the text displayed on the button to continue editing."""
        return self.continue_editing_btn.text.strip()

    @allure.step("Click close (X) button in cancel modal")
    def click_close(self):
        """Clicks the close icon (X) in the top corner of the modal."""
        self.close_btn.click()
        return self

    @allure.step("Get cancel modal warning title text")
    def get_warning_title_text(self) -> str:
        """Returns the main title text of the warning modal."""
        return self.warning_title.text.strip()

    @allure.step("Get cancel modal warning subtitle text")
    def get_warning_subtitle_text(self) -> str:
        """Returns the subtitle or secondary text of the warning modal."""
        return self.warning_subtitle.text.strip()

    @allure.step("Check if 'Yes, cancel' button is visible")
    def is_cancel_button_visible(self) -> bool:
        """Checks if the cancel confirmation button is displayed."""
        return self.yes_cancel_btn.is_displayed()

    @allure.step("Check if 'Continue editing' button is visible")
    def is_continue_editing_button_visible(self) -> bool:
        """Checks if the button to return to editing is displayed."""
        return self.continue_editing_btn.is_displayed()