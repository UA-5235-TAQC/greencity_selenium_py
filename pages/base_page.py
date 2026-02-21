from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base import Base
from components.footer_component import FooterComponent
from components.header_component import HeaderComponent
from urllib.parse import urlparse
import allure
from selenium.webdriver.remote.webelement import WebElement


class BasePage(Base):
    """ Base page class that provides common functionality for all pages. """
    HEADER = (By.XPATH, "//app-header")
    FOOTER = (By.XPATH, "//app-footer")
    TELEGRAM_CHAT = (By.CSS_SELECTOR, "button.chat-pop-up")
    MESSAGE = (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")

    def __init__(self, driver: WebDriver):
        """
        Initialize the BasePage with header component and inherit
        all base functionality from Base.
        """
        super().__init__(driver)
        _header = self.find(self.HEADER)
        _footer = self.find(self.FOOTER)
        self.header = HeaderComponent(self.driver, _header)
        self.footer = FooterComponent(self.driver, _footer)
        self.telegram = self.find(self.TELEGRAM_CHAT)

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

    @allure.step("Get header component")
    def get_header(self) -> HeaderComponent:
        return self.header

    @allure.step("Get footer component")
    def get_footer(self) -> FooterComponent:
        return self.footer

    @allure.step("Wait for snackbar message to appear")
    def wait_for_message_appear(self) -> WebElement:
        return self.wait_until_visible(self.MESSAGE)

    @allure.step("Wait for snackbar message to disappear")
    def wait_for_message_disappear(self) -> WebElement:
        return self.wait_until_invisible(self.MESSAGE)

    @allure.step("Get snackbar message text")
    def get_message_text(self) -> str:
        self.wait_for_message_appear()
        return self.get_text(*self.MESSAGE)

    def get_base_host(self) -> str:
        """ Get the base host URL with protocol and hostname for the GreenCity application. """
        current_url = self.driver.current_url
        parsed_url = urlparse(current_url)
        return f"{parsed_url.scheme}://{parsed_url.hostname}/#/greenCity"

    @allure.step("Get Telegram component")
    def get_telegram(self) -> WebElement:
        """ Get Telegram component. """
        return self.telegram

    @allure.step("Open Telegram chat")
    def open_telegram_chat(self):
        """Open Telegram chat by clicking the chat button."""
        self.click(self.TELEGRAM_CHAT)

    @allure.step("Check if Telegram chat button is visible")
    def is_telegram_chat_visible(self) -> bool:
        """Check whether chat button is visible."""
        return self.is_visible(self.TELEGRAM_CHAT)
