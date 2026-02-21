from components.base_component import BaseComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class AuthModal(BaseComponent):
    """Base class for authentication modals (Sign In / Sign Up)."""
    root_locator = (By.CSS_SELECTOR, "app-auth-modal .wrapper")

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver,
            driver.find_element(*self.root_locator)
        )
