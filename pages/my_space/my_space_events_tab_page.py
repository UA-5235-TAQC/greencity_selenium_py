from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pages.my_space.my_space_base_page import MySpaceBasePage

class MySpaceEventsTabPage(MySpaceBasePage):

    _EVENTS_HEADER = (By.CSS_SELECTOR, ".header")
    _FILTERS = (By.CSS_SELECTOR, ".events-filter")
    _EVENTS_LIST = (By.XPATH, "//div[contains(@class,'scrolling')]//app-event-item")
    _ONLINE_CHECKBOX = (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Online']]//input")
    _OFFLINE_CHECKBOX = (By.XPATH, "//mat-checkbox[.//label[normalize-space()='Offline']]//input")
    _ADD_EVENT_BUTTON = (By.ID, "create-button-event")
    _JOIN_EVENT_BUTTON = (By.ID, "create-button-join-event")
    _NO_DATA_COMPONENT = (By.CSS_SELECTOR, ".no-data app-no-data")

    def get_events_header(self):
        return self.wait.until(EC.visibility_of_element_located(self._EVENTS_HEADER))

    def get_filters(self):
        return self.wait.until(EC.visibility_of_element_located(self._FILTERS))

    def get_events(self):
        return self.driver.find_elements(*self._EVENTS_LIST)

    def get_events_count(self) -> int:
        return len(self.get_events())

    def filter_online(self):
        self.wait.until(EC.element_to_be_clickable(self._ONLINE_CHECKBOX)).click()
        return self

    def filter_offline(self):
        self.wait.until(EC.element_to_be_clickable(self._OFFLINE_CHECKBOX)).click()
        return self

    def enable_online(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self._ONLINE_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def enable_offline(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self._OFFLINE_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def click_add_event(self):
        self.wait.until(EC.element_to_be_clickable(self._ADD_EVENT_BUTTON)).click()
        return self

    def click_join_event(self):
        self.wait.until(EC.element_to_be_clickable(self._JOIN_EVENT_BUTTON)).click()
        return self