from components.base_component import BaseComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utils.page_factory import LocatorsTable


class ModalBasePage(BaseComponent):
    """Base class for authentication modals (Sign In / Sign Up)."""

    root: WebElement

    locators: LocatorsTable = {
        "root": (By.CSS_SELECTOR, "app-auth-modal .wrapper")
    }
