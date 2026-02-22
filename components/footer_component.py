import allure
from selenium.webdriver.common.by import By
from components.base_component import BaseComponent

from pages.home_page import HomePage
from pages.eco_news_page import EcoNewsPage
from pages.events_page import EventsPage
from pages.places_page import PlacesPage
from pages.about_us_page import AboutUsPage
from pages.my_space_base_page import MySpaceBasePage
from pages.ubs_courier_page import UbsCourierPage


class FooterComponent(BaseComponent):
    _logo_link = (By.CSS_SELECTOR, "a[href='#/greenCity'] img.logo")
    _news_link = (By.XPATH, ".//a[contains(@href, '#/greenCity/news')]")
    _events_link = (By.XPATH, ".//a[contains(@href, '#/greenCity/events')]")
    _places_link = (By.XPATH, ".//a[contains(@href, '#/greenCity/places')]")
    _about_link = (By.XPATH, ".//a[contains(@href, '#/greenCity/about')]")
    _my_space_link = (By.XPATH, ".//a[contains(@href, '#/greenCity/profile')]")
    _ubs_link = (By.XPATH, ".//a[contains(@href, '#/ubs')]")

    _twitter_icon = (By.CSS_SELECTOR, ".footer_social-link img[src*='twitter']")
    _linkedin_icon = (By.CSS_SELECTOR, ".footer_social-link img[src*='linkedin']")
    _facebook_icon = (By.CSS_SELECTOR, ".footer_social-link img[src*='facebook']")
    _instagram_icon = (By.CSS_SELECTOR, ".footer_social-link img[src*='instagram']")
    _youtube_icon = (By.CSS_SELECTOR, ".footer_social-link img[src*='youtube']")

    _follow_us_text = (By.CSS_SELECTOR, ".footer_follow-us span")
    _copyright_label = (By.ID, "copyright-label")

    def __init__(self, root, driver, timeout=None):
        super().__init__(root, driver, timeout)

    @allure.step("Click on footer logo")
    def click_logo_link(self):
        self.root.find_element(*self._logo_link).click()
        return HomePage(self.driver)

    @allure.step("Click on 'Eco news' link in footer")
    def click_news_link(self):
        self.root.find_element(*self._news_link).click()
        return EcoNewsPage(self.driver)

    @allure.step("Click on 'Events' link in footer")
    def click_events_link(self):
        self.root.find_element(*self._events_link).click()
        return EventsPage(self.driver)

    @allure.step("Click on 'Places' link in footer")
    def click_places_link(self):
        self.root.find_element(*self._places_link).click()
        return PlacesPage(self.driver)

    @allure.step("Click on 'About Us' link in footer")
    def click_about_link(self):
        self.root.find_element(*self._about_link).click()
        return AboutUsPage(self.driver)

    @allure.step("Click on 'My Space' link in footer")
    def click_my_space_link(self):
        self.root.find_element(*self._my_space_link).click()
        return MySpaceBasePage(self.driver)

    @allure.step("Click on 'UBS Courier' link in footer")
    def click_ubs_link(self):
        self.root.find_element(*self._ubs_link).click()
        return UbsCourierPage(self.driver)

    @allure.step("Click on Twitter icon")
    def click_twitter_icon(self):
        self.root.find_element(*self._twitter_icon).click()

    @allure.step("Click on LinkedIn icon")
    def click_linkedin_icon(self):
        self.root.find_element(*self._linkedin_icon).click()

    @allure.step("Click on Facebook icon")
    def click_facebook_icon(self):
        self.root.find_element(*self._facebook_icon).click()

    @allure.step("Click on Instagram icon")
    def click_instagram_icon(self):
        self.root.find_element(*self._instagram_icon).click()

    @allure.step("Click on YouTube icon")
    def click_youtube_icon(self):
        self.root.find_element(*self._youtube_icon).click()

    @allure.step("Get 'Follow us' text from footer")
    def get_follow_us_text(self) -> str:
        return self.root.find_element(*self._follow_us_text).text.strip()

    @allure.step("Get copyright text from footer")
    def get_copyright_text(self) -> str:
        return self.root.find_element(*self._copyright_label).text.strip()
