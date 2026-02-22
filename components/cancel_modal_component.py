from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from components.base_component import BaseComponent


class CancelModalComponent(BaseComponent):

    # locators (relative to root)
    MESSAGE_CONTAINER = (By.CSS_SELECTOR, ".warning-text")
    YES_CANCEL_BTN = (By.CSS_SELECTOR, ".buttons-container .primary-global-button")
    CONTINUE_EDITING_BTN = (By.CSS_SELECTOR, ".buttons-container .secondary-global-button")
    CLOSE_BTN = (By.CSS_SELECTOR, ".close")
    WARNING_TITLE = (By.CSS_SELECTOR, ".warning-title")
    WARNING_SUBTITLE = (By.CSS_SELECTOR, ".warning-subtitle")

    # ---------- helpers ----------

    def _find(self, locator):
        return self.root.find_element(*locator)

    def _find_all(self, locator):
        return self.root.find_elements(*locator)

    # ---------- getters ----------

    def get_message(self) -> str:
        return self._find(self.MESSAGE_CONTAINER).text.strip()

    def get_warning_title_text(self) -> str:
        return self._find(self.WARNING_TITLE).text.strip()

    def get_warning_subtitle_text(self) -> str:
        return self._find(self.WARNING_SUBTITLE).text.strip()

    def get_yes_cancel_button_text(self) -> str:
        return self._find(self.YES_CANCEL_BTN).text.strip()

    def get_continue_editing_button_text(self) -> str:
        return self._find(self.CONTINUE_EDITING_BTN).text.strip()

    # ---------- actions ----------

    def click_yes_cancel(self):
        from pages.ubs_courier_page import UbsCourierPage
        self._find(self.YES_CANCEL_BTN).click()
        return UbsCourierPage(self.get_driver())

    def click_continue_editing(self):
        self._find(self.CONTINUE_EDITING_BTN).click()

    def click_close(self):
        self._find(self.CLOSE_BTN).click()

    # ---------- state ----------

    def is_cancel_button_visible(self) -> bool:
        return self._find(self.YES_CANCEL_BTN).is_displayed()

    def is_continue_editing_button_visible(self) -> bool:
        return self._find(self.CONTINUE_EDITING_BTN).is_displayed()

    # ---------- waits ----------

    def wait_until_visible(self, timeout=10):
        WebDriverWait(self.get_driver(), timeout).until(
            EC.visibility_of(self.root)
        )
        return self

    def wait_until_closed(self, timeout=10):
        WebDriverWait(self.get_driver(), timeout).until(
            EC.invisibility_of_element(self.root)
        )