from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from base import Base

from components.header_component import HeaderComponent
from components.footer_component import FooterComponent

from selenium.webdriver.support import expected_conditions as EC
import allure
from urllib.parse import urlparse


class BasePage(Base):
    driver: WebDriver
    header_locator = (By.XPATH, "//app-header")
    footer_locator = (By.XPATH, "//app-footer")
    message_locator = (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        _header = self.driver.find_element(*self.header_locator)
        _footer = self.driver.find_element(*self.footer_locator)

        self.header = HeaderComponent(_header)
        self.footer = FooterComponent(_footer)

    def get_title(self)-> str:
        return self.driver.title

    def get_current_url(self)-> str:
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

    # components
    @allure.step("Get header component")
    def get_header(self):
        return self.header

    @allure.step("Get footer component")
    def get_footer(self):
        return self.footer

    # helpers
    @allure.step("Click on web element")
    def click(self, element):
        clickable = self.wait.until(EC.element_to_be_clickable(element))
        clickable.click()

    @allure.step("Get text from web element")
    def get_text(self, element):
        return self.wait.until(EC.visibility_of(element)).text

    # snackbar message
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