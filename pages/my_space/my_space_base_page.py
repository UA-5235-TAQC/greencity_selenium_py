import allure
from selenium.webdriver.common.by import By

from components.my_space.profile_panel_component import ProfilePanelComponent
from pages.base_page import BasePage
from utils.page_factory import LocatorsTable


class MySpaceBasePage(BasePage):
    """ Base Page Object for the 'My Space' (Profile) page in the application. """

    profile_panel: ProfilePanelComponent

    locators: LocatorsTable = {
        "profile_panel": (By.XPATH, "//div[@class='left-column']")
    }

    @allure.step("Open My Space Page")
    def open(self) -> "MySpaceBasePage":
        """ Navigate to the My Space (Profile) page. """
        self.driver.get(self.get_base_host() + "/profile")
        return self

    @allure.step("Check if My Space Page is opened")
    def is_page_opened(self) -> bool:
        """ Verify that the My Space page is opened. """
        return self.profile_panel.is_component_visible()
