from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

from components.stat_row_component import StatRowComponent
from components.subscribe_component import SubscribeComponent

import allure

class HomePage(BasePage):
    driver: WebDriver

    root = (By.CSS_SELECTOR, "main")
    hero_title = (By.CSS_SELECTOR, ".main-content h1")
    hero_description = (By.CSS_SELECTOR, "#header-left p")
    start_habit_button = (By.CSS_SELECTOR, "#header-left button.primary-global-button")
    stats_section = (By.CSS_SELECTOR, "#stats")
    eco_news_section = (By.CSS_SELECTOR, "#events")
    subscription_section = (By.CSS_SELECTOR, ".subscribe-container")
    email_input = (By.CSS_SELECTOR, ".subscription-input")
    subscribe_button = (By.CSS_SELECTOR, "div #subscribe")
    read_all_news_link = (By.CSS_SELECTOR, ".eco-events a")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._stat_row_component_list: list[StatRowComponent] = []
        self._subscribe_component: SubscribeComponent = None

    @allure.step("Check that home page is opened")
    def is_page_opened(self) -> bool:
        return self.is_visible(self.root)

    @allure.step("Wait until home page is loaded")
    def wait_until_opened(self) -> "HomePage":
        self.wait_until_visible(self.root)
        return self

    @allure.step("Open home page")
    def open(self) -> "HomePage":
        self.driver.get(self.get_base_host())
        return self.wait_until_opened()

    @allure.step("Get hero title text")
    def get_hero_title(self) -> str:
        return self.get_text(self.hero_title)

    @allure.step("Get hero description text")
    def get_hero_description(self) -> str:
        return self.get_text(self.hero_description)

    @allure.step("Click 'Start habit' button")
    def click_start_habit(self):
        self.click(self.start_habit_button)

    @allure.step("Get statistics section text")
    def get_stats(self) -> str:
        return self.get_text(self.stats_section)

    @allure.step("Get eco news preview text")
    def get_eco_news_preview(self) -> str:
        return self.get_text(self.eco_news_section)

    @allure.step("Click 'Read all news' link")
    def click_read_all_news(self):
        self.click(self.read_all_news_link)

    @allure.step("Subscribe with email: {email}")
    def subscribe(self, email: str):
        email_input = self.wait_until_visible(self.email_input)
        email_input.send_keys(email)

        self.wait_until_visible(self.subscribe_button).click()

    @allure.step("Get statistics row components list")
    def get_stat_row_component_list(self) -> list[StatRowComponent]:
        return self._stat_row_component_list

    @allure.step("Get subscribe component")
    def get_subscribe_component(self) -> SubscribeComponent:
        return self._subscribe_component