from urllib.parse import urlparse

import allure
from selenium.webdriver.remote.webelement import WebElement

from components.footer_component import FooterComponent
from components.header_component import HeaderComponent
from utils.page_factory import (PageFactory, LocatorsTable, By)


class BasePage(PageFactory):
    """ Base page class that provides common functionality for all pages. """

    header: HeaderComponent
    footer: FooterComponent
    telegram: WebElement
    message: WebElement

    locators: LocatorsTable = {
        "header": (By.XPATH, "//app-header", HeaderComponent),
        "footer": (By.XPATH, "//app-footer", FooterComponent),
        "telegram": (By.CSS_SELECTOR, "button.chat-pop-up"),
        "message": (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")
    }

    def __init__(self, driver):
        all_locators = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'locators'):
                all_locators.update(cls.locators)

        self.locators = all_locators

        super().__init__(driver)

    @allure.step("Get the title of the current page")
    def get_title(self) -> str:
        """Return the title of the current page."""
        return self.driver.title

    @allure.step("Get the current URL of the page")
    def get_current_url(self) -> str:
        """Return the current URL of the page."""
        return self.driver.current_url

    @allure.step("Open page")
    def open(self):
        raise NotImplementedError

    @allure.step("Check that page is opened")
    def is_page_opened(self):
        raise NotImplementedError

    @allure.step("Wait until page is fully opened")
    def wait_until_opened(self):
        raise NotImplementedError

    @allure.step("Get snackbar message text")
    def get_message_text(self) -> str:
        return self.message.text

    def get_base_host(self) -> str:
        """ Get the base host URL with protocol and hostname for the GreenCity application. """
        current_url = self.driver.current_url
        parsed_url = urlparse(current_url)
        return f"{parsed_url.scheme}://{parsed_url.hostname}/#/greenCity"

    @allure.step("Open Telegram chat")
    def open_telegram_chat(self):
        """Open Telegram chat by clicking the chat button."""
        self.telegram.click()
        self.click(self.TELEGRAM_CHAT)
