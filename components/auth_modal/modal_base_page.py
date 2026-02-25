from components.base_component import BaseComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class ModalBasePage(BaseComponent):
    """Base class for authentication modals (Sign In / Sign Up)."""
    root_locator = (By.CSS_SELECTOR, "app-auth-modal .wrapper")

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver,
            self.find(*self.root_locator)
        )
