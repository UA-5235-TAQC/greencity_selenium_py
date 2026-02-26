from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from utils.page_factory import LocatorsTable
import allure


class HomePage(BasePage):
    """Concrete implementation of the Home Page."""

    root: WebElement
    hero_title: WebElement
    hero_description: WebElement
    start_habit_btn: WebElement
    stats_section: WebElement
    eco_news_section: WebElement
    subscription_section: WebElement
    email_input: WebElement
    subscribe_btn: WebElement
    read_all_news_link: WebElement

    locators: LocatorsTable = {
        "root": (By.CSS_SELECTOR, ".main-content"),
        "hero_title": (By.CSS_SELECTOR, ".main-content h1"),
        "hero_description": (By.CSS_SELECTOR, "#header-left p"),
        "start_habit_btn": (By.CSS_SELECTOR, "#header-left button.primary-global-button"),
        "stats_section": (By.CSS_SELECTOR, "#stats"),
        "eco_news_section": (By.CSS_SELECTOR, "#events"),
        "subscription_section": (By.CSS_SELECTOR, "#subscription"),
        "email_input": (By.CSS_SELECTOR, "input[type='email']"),
        "subscribe_btn": (By.CSS_SELECTOR, "div #subscribe"),
        "read_all_news_link": (By.CSS_SELECTOR, ".eco-events a"),
    }

    @allure.step("Check that home page is opened")
    def is_page_opened(self) -> bool:
        """ Check that home page is opened. """
        return self.root.is_displayed()

    @allure.step("Wait until home page is loaded")
    def wait_until_opened(self) -> "HomePage":
        """ Wait until home page is visible. """
        self.wait_until_visible(self.root)
        return self

    @allure.step("Open home page")
    def open(self) -> "HomePage":
        """ Open home page. """
        self.driver.get(self.get_base_host())
        return self.wait_until_opened()

    @allure.step("Get hero title text")
    def get_hero_title(self) -> str:
        """ Get hero title text. """
        return self.hero_title.text

    @allure.step("Get hero description text")
    def get_hero_description(self) -> str:
        """ Get hero description text. """
        return self.hero_description.text

    @allure.step("Click 'Start habit' button")
    def click_start_habit(self):
        """ Click 'Start habit' button. """
        self.start_habit_btn.click()

    @allure.step("Get statistics section text")
    def get_stats(self) -> str:
        """ Get statistics section text. """
        return self.stats_section.text

    @allure.step("Get eco news section text")
    def get_eco_news_section(self) -> str:
        """ Get eco news section text. """
        return self.eco_news_section.text

    @allure.step("Click 'Read all news' link")
    def click_read_all_news(self):
        """ Click 'Read all news' link. """
        self.read_all_news_link.click()

    @allure.step("Subscribe with email: {email}")
    def subscribe(self, email: str):
        """ Subscribe with email. """
        self.email_input.send_keys(email)
        self.subscribe_btn.click()
