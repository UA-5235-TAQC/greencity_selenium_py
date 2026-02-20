from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.header_component import HeaderComponent


class BasePage:
    driver: WebDriver
    header: HeaderComponent
    header_locator = (By.XPATH, "//app-header")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        _header = self.driver.find_element(*self.header_locator)
        self.header = HeaderComponent(_header)

    def get_title(self)-> str:
        return self.driver.title

    def get_current_url(self)-> str:
        return self.driver.current_url