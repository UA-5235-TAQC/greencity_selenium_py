from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable


class MySpaceEventsTabPage(MySpaceBasePage):
    """ Page Object representing the 'My events' tab in My Space page. """

    events_header: WebElement
    filters: WebElement
    events_items: List[WebElement]
    online_checkbox: WebElement
    offline_checkbox: WebElement
    add_event_button: WebElement
    join_event_button: WebElement

    locators: LocatorsTable = {
        "events_header": (By.CSS_SELECTOR, "mat-tab-body.mat-mdc-tab-body-active .header"),
        "filters": (By.CSS_SELECTOR, ".events-filter"),
        "events_items": (By.CSS_SELECTOR, "ul.news-list > li"),
        "online_checkbox": (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Online']]//input"),
        "offline_checkbox": (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Offline']]//input"),
        "add_event_button": (By.ID, "create-button-event"),
    }

    @allure.step("Get events count")
    def get_events_count(self) -> int:
        """ Get events count. """
        return len(self.events_items)

    @allure.step("Filter online events")
    def filter_online(self):
        """ Filter online events. """
        self.online_checkbox.click()
        return self

    @allure.step("Filter offline events")
    def filter_offline(self):
        """ Filter offline events. """
        self.offline_checkbox.click()
        return self

    @allure.step("Enable online filter")
    def enable_online(self):
        """ Enable online filter. """
        if not self.online_checkbox.is_selected():
            self.online_checkbox.click()
        return self

    @allure.step("Enable offline filter")
    def enable_offline(self):
        """ Enable offline filter. """
        if not self.offline_checkbox.is_selected():
            self.offline_checkbox.click()
        return self

    @allure.step("Click Add Event button")
    def click_add_event(self):
        """ Click Add Event button. """
        self.add_event_button.click()
        return self
