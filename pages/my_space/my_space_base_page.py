from typing import List

import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.my_space.calendar_component import CalendarComponent
from components.my_space.profile_panel_component import ProfilePanelComponent
from components.my_space.to_do_list_component import ToDoListComponent
from enums.my_space_tab import MySpaceTab
from pages.base_page import BasePage
from utils.page_factory import LocatorsTable


class MySpaceBasePage(BasePage):
    """ Base Page Object for the 'My Space' (Profile) page in the application. """

    profile_panel: ProfilePanelComponent
    tabs: List[WebElement]
    calendar: CalendarComponent
    to_do_list: ToDoListComponent
    fact_of_the_day: WebElement
    active_tab: WebElement

    locators: LocatorsTable = {
        "profile_panel": (By.XPATH, "//div[@class='left-column']", ProfilePanelComponent),
        "tabs": (By.CSS_SELECTOR, ".mat-mdc-tab-labels div", List[WebElement]),
        "calendar": (By.CLASS_NAME, "app-calendar", CalendarComponent),
        "to_do_list": (By.CLASS_NAME, "app-to-do-list", ToDoListComponent),
        "fact_of_the_day": (By.XPATH, "//p[@class='card-description']"),
        "active_tab": (By.XPATH, "//div[@role='tab' and @aria-selected='true']"),
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

    @allure.step("Wait until My Space Page is loaded")
    def wait_until_opened(self) -> "MySpaceBasePage":
        """Explicitly waits for the profile panel to become visible via PageFactory."""
        self.profile_panel.is_visible()
        return self

    @allure.step("Get fact of the day")
    def get_fact_of_the_day(self) -> str:
        """Returns the text of the 'Fact of the Day' card."""
        return self.fact_of_the_day.text.strip()

    @allure.step("Get list of tabs")
    def get_tab_list(self) -> List[str]:
        """Returns a list of all visible tab names in the profile navigation bar"""
        return [tab.text.strip() for tab in self.tabs if tab.is_displayed()]

    @allure.step("Get active tab")
    def get_active_tab(self) -> str:
        """Returns the name of the currently selected tab."""
        return self.active_tab.text.strip()

    @allure.step("Switch to tab")
    def switch_to(self, tab: MySpaceTab) -> "MySpaceBasePage":
        """ Switches to the specified tab by clicking on it"""
        for el in self.tabs:
            if tab.matches(el.text):
                el.click()
                return self
        raise NoSuchElementException(f"Tab not found: {tab}")
