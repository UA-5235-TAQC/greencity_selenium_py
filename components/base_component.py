import allure

from data.config import Config
from utils.page_factory import PageFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseComponent(PageFactory):
    """ Base class for page components. """

    def __init__(self, driver):
        """ Initialize the base component with a WebDriver instance and merge all declared locators. """
        all_locators = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'locators'):
                all_locators.update(cls.locators)

        self.locators = all_locators
        super().__init__(driver)

    @allure.step("Check if the component is enabled")
    def is_enabled(self) -> bool:
        """Check if the component is enabled."""
        return self.root_element.is_enabled()

    @allure.step("Check if the component is visible")
    def is_visible(self) -> bool:
        """Check if the component is visible."""
        return self.root_element.is_displayed()

    @allure.step("Wait until cancel modal is closed")
    def wait_until_closed(self, timeout: int = Config.EXPLICITLY_WAIT):
        """ Waits until the cancel modal is no longer visible on the page. """
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element(self.root_element)
        )
        return self

    @allure.step("Wait for a custom lambda condition.")
    def wait_for(self, condition, timeout=None):
        """Wait for a custom lambda condition."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(condition)
