from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from pages.news_details_page import NewsDetailsPage
from utils.page_factory import LocatorsTable
from typing import List
import allure


class MySpaceNewsItemComponent(BaseComponent):

    news_container: WebElement
    image_element: WebElement
    title_element: WebElement
    creation_date_element: WebElement
    author_name_element: WebElement
    tags_locator: tuple[str, str] = (By.CSS_SELECTOR, ".tags .tag-btn")

    locators: LocatorsTable = {
        "news_container": (By.CSS_SELECTOR, "div.news"),
        "image_element": (By.CSS_SELECTOR, ".news-image"),
        "title_element": (By.CSS_SELECTOR, ".title h3"),
        "creation_date_element": (By.CSS_SELECTOR, ".user-info-date p"),
        "author_name_element": (By.CSS_SELECTOR, ".user-info-icon p"),
    }


    def __init__(self, root_element: WebElement, news_id: int):
        super().__init__(root_element)
        self.news_id = news_id


    @allure.step("Get news id")
    def get_id(self) -> int:
        """Returns the WebElement of the news image"""
        return self.news_id

    @allure.step("Get image element")
    def get_image_element(self) -> WebElement:
        """Returns the WebElement of the news image"""
        return self.image_element

    @allure.step("Get image src")
    def get_image_src(self) -> str:
        """Gets the source URL of the news image."""
        return self.image_element.get_attribute("src")

    @allure.step("Get tag elements")
    def get_tag_elements(self) -> List[WebElement]:
        return self.root_element.find_elements(*self.tags_locator)

    @allure.step("Get tags text")
    def get_tags(self) -> List[str]:
        """Returns a list of WebElements for the tags associated with the news"""
        return [
            tag.text.strip()
            for tag in self.get_tag_elements()
        ]

    @allure.step("Get title element")
    def get_title_element(self) -> WebElement:
        """Returns the WebElement of the news title"""
        return self.title_element

    @allure.step("Get elements title ")
    def get_title(self) -> str:
        """Gets the text content of the news title."""
        return self.title_element.text.strip()

    @allure.step("Get creation date element")
    def get_creation_date_element(self) -> WebElement:
        """Returns the WebElement containing the creation date"""
        return self.creation_date_element

    @allure.step("Get creation date")
    def get_creation_date(self) -> str:
        """Gets the displayed creation date text"""
        return self.creation_date_element.text.strip()

    @allure.step("Get author name element")
    def get_author_name_element(self) -> WebElement:
        """Returns the WebElement containing the author's name"""
        return self.author_name_element

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        """Gets the text content of the author's name"""
        return self.author_name_element.text.strip()

    @allure.step("Open news details page")
    def click(self) -> NewsDetailsPage:
        """Clicks on the news card and navigates to the details page."""
        self.news_container.click()
        return NewsDetailsPage(self.driver, self.news_id)