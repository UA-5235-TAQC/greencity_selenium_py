from typing import List
import allure
from selenium.webdriver.common.by import By
from components.base_component import BaseComponent


class CalendarComponent(BaseComponent):
    """
    UI component that represents the calendar widget
    in the "My Space" section.
    """

    PREVIOUS_MONTH_BUTTON = (By.CSS_SELECTOR, "img.arrow-previous")
    NEXT_MONTH_BUTTON = (By.CSS_SELECTOR, "img.arrow-next")
    MONTH_AND_YEAR_LABEL = (By.CSS_SELECTOR, "button.monthAndYear")
    DAYS_OF_WEEK = (By.CSS_SELECTOR, ".days-name")
    CALENDAR_DAYS = (By.CSS_SELECTOR, ".calendar-grid-day")
    CURRENT_DAY = (By.CSS_SELECTOR, ".calendar-grid-day.current-day span")
    CURRENT_DAY_OF_WEEK = (By.CSS_SELECTOR, ".days-name.current-day-name")
    DAY_NUMBER = (By.TAG_NAME, "span")

    @allure.step("Click previous month")
    def click_previous_month(self) -> None:
        """ Click previous month. """
        self.click(self.PREVIOUS_MONTH_BUTTON)

    @allure.step("Click next month")
    def click_next_month(self) -> None:
        """ Click next month. """
        self.click(self.NEXT_MONTH_BUTTON)

    @allure.step("Get month and year as a text")
    def get_month_and_year(self) -> str:
        """ Get month and year as a text. """
        return self.get_text(self.MONTH_AND_YEAR_LABEL)

    @allure.step("Get current month name")
    def get_month(self) -> str:
        """ Get current month name. """
        return self.get_month_and_year().split()[0]

    @allure.step("Get current year")
    def get_year(self) -> int:
        """ Get current year. """
        return int(self.get_month_and_year().split()[1])

    @allure.step("Get visible calendar days")
    def get_visible_days(self) -> List[int]:
        """ Get all visible calendar days as integers. """
        texts = self.get_texts_from(self.DAY_NUMBER)
        return [int(text) for text in texts if text.isdigit()]

    @allure.step("Get current selected day")
    def get_current_day(self) -> int:
        """ Get current selected day. """
        return int(self.get_text(self.CURRENT_DAY))

    @allure.step("Select day {day}")
    def select_day(self, day: int) -> None:
        """ Select a specific day in the calendar. """
        days_texts = self.get_texts_from(self.CALENDAR_DAYS)
        for idx, text in enumerate(days_texts):
            if text == str(day):
                self.find_all_from(self.root, self.CALENDAR_DAYS)[idx].click()
                return
        raise RuntimeError(f"Day not found: {day}")

    @allure.step("Get days of week names")
    def get_days_of_week(self) -> List[str]:
        """ Retrieve the names of the days of the week displayed in the calendar header. """
        return self.get_texts_from(self.DAYS_OF_WEEK)

    @allure.step("Get current day of week")
    def get_day_of_week(self) -> str:
        """ Get the name of the currently selected day of the week. """
        return self.get_text(self.CURRENT_DAY_OF_WEEK)

    @allure.step("Check if calendar is visible")
    def is_visible(self) -> bool:
        """ Check whether the calendar component is visible on the page. """
        return self.is_visible(self.CALENDAR_DAYS)
