import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.page_factory import LocatorsTable
from pages.base_page import BasePage


class UbsCourierPage(BasePage):
    """Page Object representing the UBS Courier page."""

    partners_section: WebElement
    read_all_news_link: WebElement

    locators: LocatorsTable = {
        "partners_section": (By.CSS_SELECTOR, "div.our-partners-section__icons"),
        "read_all_news_link": (By.CSS_SELECTOR, "section#events a[href*='greenCity/news']"),
    }

    @allure.step("Open UBS Courier page")
    def open(self):
        """ Open UBS Courier page. """
        self.driver.get(f"{self.get_base_host()}/ubs/")
        return self

    @allure.step("Check that UBS Courier page is opened")
    def is_page_opened(self) -> bool:
        """ Check that UBS Courier page is opened. """
        return self.partners_section.is_displayed()

    @allure.step("Check page opened after cancel modal click Yes/Cancel")
    def is_page_opened_after_cancel_modal_click_yes_cancel(self) -> bool:
        """ Check page opened after cancel modal click Yes/Cancel. """
        return self.read_all_news_link.is_displayed()

    @allure.step("Wait until UBS Courier page is opened")
    def wait_until_opened(self):
        """ Wait until UBS Courier page is opened. """
        self.wait_until_visible(self.partners_section)
        return self
