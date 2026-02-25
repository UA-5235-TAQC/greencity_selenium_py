from __future__ import annotations
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable


class FooterComponent(BaseComponent):
    """Component representing the footer section present across the application."""

    logo_link: WebElement
    news_link: WebElement
    events_link: WebElement
    places_link: WebElement
    about_link: WebElement
    my_space_link: WebElement
    ubs_link: WebElement
    twitter_icon: WebElement
    linkedin_icon: WebElement
    facebook_icon: WebElement
    instagram_icon: WebElement
    youtube_icon: WebElement
    follow_us_text_element: WebElement
    copyright_label: WebElement

    locators: LocatorsTable = {
        "logo_link": (By.CSS_SELECTOR, "a[href='#/greenCity'] img.logo"),
        "news_link": (By.XPATH, ".//a[contains(@href, '#/greenCity/news')]"),
        "events_link": (By.XPATH, ".//a[contains(@href, '#/greenCity/events')]"),
        "places_link": (By.XPATH, ".//a[contains(@href, '#/greenCity/places')]"),
        "about_link": (By.XPATH, ".//a[contains(@href, '#/greenCity/about')]"),
        "my_space_link": (By.XPATH, ".//a[contains(@href, '#/greenCity/profile')]"),
        "ubs_link": (By.XPATH, ".//a[contains(@href, '#/ubs')]"),
        "twitter_icon": (By.CSS_SELECTOR, ".footer_social-link img[src*='twitter']"),
        "linkedin_icon": (By.CSS_SELECTOR, ".footer_social-link img[src*='linkedin']"),
        "facebook_icon": (By.CSS_SELECTOR, ".footer_social-link img[src*='facebook']"),
        "instagram_icon": (By.CSS_SELECTOR, ".footer_social-link img[src*='instagram']"),
        "youtube_icon": (By.CSS_SELECTOR, ".footer_social-link img[src*='youtube']"),
        "follow_us_text_element": (By.CSS_SELECTOR, ".footer_follow-us span"),
        "copyright_label": (By.ID, "copyright-label")
    }

    @allure.step("Click on footer logo")
    def click_logo_link(self):
        """Clicks the logo in the footer to navigate to the Home Page."""
        self.logo_link.click()
        from pages.home_page import HomePage
        return HomePage(self.driver)

    @allure.step("Click on 'Eco news' link in footer")
    def click_news_link(self):
        """Clicks the 'Eco news' link in the footer."""
        self.news_link.click()
        from pages.news_page import NewsPage
        return NewsPage(self.driver)

    @allure.step("Click on 'Events' link in footer")
    def click_events_link(self):
        """Clicks the 'Events' link in the footer."""
        self.events_link.click()
        # from pages.events_page import EventsPage
        # return EventsPage(self.driver)

    @allure.step("Click on 'Places' link in footer")
    def click_places_link(self):
        """Clicks the 'Places' link in the footer."""
        self.places_link.click()
        # from pages.places_page import PlacesPage
        # return PlacesPage(self.driver)

    @allure.step("Click on 'About Us' link in footer")
    def click_about_link(self):
        """Clicks the 'About Us' link in the footer."""
        self.about_link.click()
        # from pages.about_us_page import AboutUsPage
        # return AboutUsPage(self.driver)

    @allure.step("Click on 'My Space' link in footer")
    def click_my_space_link(self):
        """Clicks the 'My Space' (profile) link in the footer."""
        self.my_space_link.click()
        # from pages.my_space_base_page import MySpaceBasePage
        # return MySpaceBasePage(self.driver)

    @allure.step("Click on 'UBS Courier' link in footer")
    def click_ubs_link(self):
        """Clicks the 'UBS Courier' link in the footer."""
        self.ubs_link.click()
        # from pages.ubs_courier_page import UbsCourierPage
        # return UbsCourierPage(self.driver)

    @allure.step("Click on Twitter icon")
    def click_twitter_icon(self):
        """Clicks the Twitter social media icon."""
        self.twitter_icon.click()
        return self

    @allure.step("Click on LinkedIn icon")
    def click_linkedin_icon(self):
        """Clicks the LinkedIn social media icon."""
        self.linkedin_icon.click()
        return self

    @allure.step("Click on Facebook icon")
    def click_facebook_icon(self):
        """Clicks the Facebook social media icon."""
        self.facebook_icon.click()
        return self

    @allure.step("Click on Instagram icon")
    def click_instagram_icon(self):
        """Clicks the Instagram social media icon."""
        self.instagram_icon.click()
        return self

    @allure.step("Click on YouTube icon")
    def click_youtube_icon(self):
        """Clicks the YouTube social media icon."""
        self.youtube_icon.click()
        return self

    @allure.step("Get 'Follow us' text from footer")
    def get_follow_us_text(self) -> str:
        """Returns the trimmed text from the 'Follow us' section."""
        return self.follow_us_text_element.text.strip()

    @allure.step("Get copyright text from footer")
    def get_copyright_text(self) -> str:
        """Returns the trimmed copyright text from the footer."""
        return self.copyright_label.text.strip()