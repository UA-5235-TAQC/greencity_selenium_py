from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base import Base
from components.footer_component import FooterComponent
from components.header_component import HeaderComponent
from urllib.parse import urlparse
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class BasePage(Base):
    """ Base page class that provides common functionality for all pages. """
    header_locator = (By.XPATH, "//app-header")
    footer_locator = (By.XPATH, "//app-footer")
    message_locator = (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")

    def __init__(self, driver: WebDriver):
        """
        Initialize the BasePage with header component and inherit
        all base functionality from Base.
        """
        super().__init__(driver)
        _header = self.driver.find_element(*self.header_locator)
        _footer = self.driver.find_element(*self.footer_locator)
        self.header = HeaderComponent(self.driver, _header)
        self.footer = FooterComponent(self.driver, _footer)

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

    @allure.step("Click on web element")
    def click(self, element: WebElement):
        clickable = self.wait.until(EC.element_to_be_clickable(element))
        clickable.click()

    @allure.step("Get text from web element")
    def get_text(self, element: WebElement) -> str:
        return self.wait.until(EC.visibility_of(element)).text

    @allure.step("Wait for snackbar message to appear")
    def wait_for_message_appear(self):
        self.wait.until(EC.visibility_of_element_located(self.message_locator))
        return self

    @allure.step("Wait for snackbar message to disappear")
    def wait_for_message_disappear(self):
        self.wait.until(EC.invisibility_of_element_located(self.message_locator))
        return self

    @allure.step("Get snackbar message text")
    def get_message_text(self):
        self.wait_for_message_appear()
        return self.driver.find_element(*self.message_locator).text

    def get_base_host(self) -> str:
        """ Get the base host URL with protocol and hostname for the GreenCity application. """
        current_url = self.driver.current_url
        parsed_url = urlparse(current_url)
        return f"{parsed_url.scheme}://{parsed_url.hostname}/#/greenCity"
