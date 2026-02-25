from typing import List

import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.my_space.profile_panel_component import ProfilePanelComponent
from enums.my_space_tab import MySpaceTab
from pages.base_page import BasePage
from utils.page_factory import LocatorsTable


class MySpaceBasePage(BasePage):
    """ Base Page Object for the 'My Space' (Profile) page in the application. """

    profile_panel: WebElement
    tabs_container: WebElement
    calendar: WebElement
    to_do_list_block: WebElement
    fact_of_the_day_element: WebElement
    user_rating_element: WebElement
    user_name_element: WebElement
    active_tab_element: WebElement
    edit_profile_btn: WebElement
    todo_count_element: WebElement
    todo_items_locator: tuple[str, str] = (By.CSS_SELECTOR, ".right-column .item")
    tab_list_locator: tuple[str, str] = (By.CSS_SELECTOR, ".mat-mdc-tab-labels div")

    locators: LocatorsTable = {
        "profile_panel": (By.XPATH, "//div[@class='left-column']"),
        "tabs_container": (By.XPATH, "//div[@role='tablist']"),
        "calendar": (By.CLASS_NAME, "app-calendar"),
        "to_do_list_block": (By.XPATH, "(//div[@class='to-do-list-block'])[2]"),
        "fact_of_the_day_element": (By.XPATH, "//p[@class='card-description']"),
        "user_rating_element": (By.XPATH, "//div[@class='rate']//p"),
        "user_name_element": (By.CSS_SELECTOR, ".left-column .name"),
        "active_tab_element": (By.XPATH, "//div[@role='tab' and @aria-selected='true']"),
        "edit_profile_btn": (By.CSS_SELECTOR, ".main-content.app-container"),
        "todo_count_element": (By.XPATH, "(//div[@class='items-count'])[2]"),
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
        self.profile_panel.is_displayed()
        return self

    @allure.step("Get profile panel component")
    def get_profile_panel(self) -> ProfilePanelComponent:
        """Returns a component object for the side profile panel."""
        return ProfilePanelComponent(self.profile_panel)

    @allure.step("Get fact of the day")
    def get_fact_of_the_day(self) -> str:
        """Returns the text of the 'Fact of the Day' card."""
        return self.fact_of_the_day_element.text.strip()

    @allure.step("Get user rating")
    def get_user_rating(self) -> str:
        """Returns the user's current rating value."""
        return self.user_rating_element.text.strip()

    @allure.step("Get user name")
    def get_user_name(self) -> str:
        """Returns the displayed name from the profile panel."""
        return self.user_name_element.text.strip()

    @allure.step("Open edit profile page")
    def open_profile(self) -> None:
        """Clicks on the profile edit button to navigate to settings."""
        self._click(self.edit_profile_btn)

    @allure.step("Get list of to-do items")
    def get_to_do_items(self) -> List[str]:
        """Checks the task counter and returns a list of task names if available."""
        count_text = self.todo_count_element.text

        digits_only = "".join(char for char in count_text if char.isdigit())
        total = int(digits_only) if digits_only else 0

        if total == 0:
            return []

        items = self.driver.find_elements(*self.todo_items_locator)
        return [el.text.strip() for el in items]

    @allure.step("Get list of tabs")
    def get_tab_list(self) -> List[str]:
        """Returns a list of all visible tab names in the profile navigation bar"""
        self.tabs_container.is_displayed()
        tabs = self.driver.find_elements(*self.tab_list_locator)
        return [tab.text.strip() for tab in tabs if tab.is_displayed()]

    @allure.step("Get active tab")
    def get_active_tab(self) -> str:
        """Returns the name of the currently selected tab."""
        return self.active_tab_element.text.strip()

    @allure.step("Switch to tab")
    def switch_to(self, tab: MySpaceTab) -> "MySpaceBasePage":
        """ Switches to the specified tab by clicking on it"""
        self.tabs_container.is_displayed()

        tabs = self.driver.find_elements(*self.tab_list_locator)
        for el in tabs:
            if tab.matches(el.text):
                el.click()
                return self

        raise NoSuchElementException(f"Tab not found: {tab}")
