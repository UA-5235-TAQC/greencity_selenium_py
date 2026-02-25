from typing import List
import allure
from selenium.webdriver.common.by import By
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from selenium.webdriver.remote.webelement import WebElement


class CalendarComponent(BaseComponent):
    """
    UI component that represents the calendar widget
    in the "My Space" section.
    """

    previous_month_btn: WebElement
    next_month_btn: WebElement
    month_and_year_label: WebElement
    days_of_week: List[WebElement]
    calendar_days: List[WebElement]
    current_day: WebElement
    current_day_of_week: WebElement
    day_number: WebElement

    locators: LocatorsTable = {
        "previous_month_btn": (By.CSS_SELECTOR, "img.arrow-previous"),
        "next_month_btn": (By.CSS_SELECTOR, "img.arrow-next"),
        "month_and_year_label": (By.CSS_SELECTOR, "button.monthAndYear"),
        "days_of_week": (By.CSS_SELECTOR, ".days-name"),
        "calendar_days": (By.CSS_SELECTOR, ".calendar-grid-day"),
        "current_day": (By.CSS_SELECTOR, ".calendar-grid-day.current-day span"),
        "current_day_of_week": (By.CSS_SELECTOR, ".days-name.current-day-name"),
        "day_number": (By.TAG_NAME, "span")
    }

    @allure.step("Click previous month")
    def click_previous_month(self):
        """ Click previous month. """
        self.previous_month_button.click()

    @allure.step("Click next month")
    def click_next_month(self):
        """ Click next month. """
        self.next_month_button.click()

    @allure.step("Get month and year as a text")
    def get_month_and_year(self) -> str:
        """ Get month and year as a text. """
        return self.month_and_year_label.text

    @allure.step("Get current month name")
    def get_month(self) -> str:
        """ Get current month name. """
        return self.get_month_and_year().split()[0]

    @allure.step("Get current year")
    def get_year(self) -> int:
        """ Get current year. """
        return int(self.get_month_and_year().split()[1])

    @allure.step("Get all visible days in the calendar")
    def get_visible_days(self) -> List[int]:
        """ Get all visible calendar days as integers. """
        days: List[WebElement] = self.calendar_days
        visible_days = []
        for day in days:
            span_text = day.find_element(By.TAG_NAME, "span").text.strip()
            if span_text:
                visible_days.append(int(span_text))
        return visible_days

    @allure.step("Get current selected day")
    def get_current_day(self) -> int:
        """ Get current selected day. """
        return int(self.current_day.text)

    @allure.step("Select day {day} in the calendar")
    def select_day(self, day: int) -> None:
        """ Select a specific day in the calendar. """
        for d in self.calendar_days:
            if d.text.strip() == str(day):
                d.click()
                return
        raise RuntimeError(f"Day not found: {day}")

    @allure.step("Get names of the days of the week")
    def get_days_of_week(self) -> List[str]:
        """ Retrieve the names of the days of the week displayed in the calendar header. """
        return [el.text.strip() for el in self.days_of_week]

    @allure.step("Get current day of week")
    def get_day_of_week(self) -> str:
        """ Get the name of the currently selected day of the week. """
        return self.current_day_of_week.text

    @allure.step("Check if calendar is visible")
    def is_visible(self) -> bool:
        """ Check whether the calendar component is visible on the page. """
        return self.month_and_year_label.is_displayed()
