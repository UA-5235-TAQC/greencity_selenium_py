from typing import List
import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable

class MySpaceEventsTabPage(MySpaceBasePage):
    events_header: WebElement
    filters: WebElement
    events_items: List[WebElement]
    online_checkbox: WebElement
    offline_checkbox: WebElement
    add_event_button: WebElement
    join_event_button: WebElement
    no_data_component: WebElement

    locators: LocatorsTable = {
        "events_header": (By.CSS_SELECTOR, ".header"),
        "filters": (By.CSS_SELECTOR, ".events-filter"),
        "events_items": (By.CSS_SELECTOR, "app-event-item"),
        "online_checkbox": (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Online']]//input"),
        "offline_checkbox": (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Offline']]//input"),
        "add_event_button": (By.ID, "create-button-event"),
        "join_event_button": (By.ID, "create-button-join-event"),
        "no_data_component": (By.CSS_SELECTOR, ".no-data app-no-data"),
    }

    @allure.step("Get events")
    def get_events(self) -> List[WebElement]:
        return self.events_items

    @allure.step("Get events count")
    def get_events_count(self) -> int:
        return len(self.events_items)

    @allure.step("Filter online events")
    def filter_online(self):
        self.online_checkbox.click()
        return self

    @allure.step("Filter offline events")
    def filter_offline(self):
        self.offline_checkbox.click()
        return self

    @allure.step("Enable online filter")
    def enable_online(self):
        if not self.online_checkbox.is_selected():
            self.online_checkbox.click()
        return self

    @allure.step("Enable offline filter")
    def enable_offline(self):
        if not self.offline_checkbox.is_selected():
            self.offline_checkbox.click()
        return self

    @allure.step("Click Add Event button")
    def click_add_event(self):
        self.add_event_button.click()
        return self

    @allure.step("Click Join Event button")
    def click_join_event(self):
        self.join_event_button.click()
        return self