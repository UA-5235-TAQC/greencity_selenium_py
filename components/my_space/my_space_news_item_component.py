from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from pages.news_details_page import NewsDetailsPage


class MySpaceNewsItemComponent(BaseComponent):
    news_container_locator = (By.CSS_SELECTOR, "div.news")
    image_locator = (By.CSS_SELECTOR, ".news-image")
    tags_locator = (By.CSS_SELECTOR, ".tags .tag-btn")
    title_locator = (By.CSS_SELECTOR, ".title h3")
    creation_date_locator = (By.CSS_SELECTOR, ".user-info-date p")
    author_name_locator = (By.CSS_SELECTOR, ".user-info-icon p")

    def __init__(self, driver: WebDriver, root: WebElement, news_id: int, timeout):
        super().__init__(root, driver, timeout)
        self.news_id = news_id


    def get_id(self) -> int:
        return self.news_id

    def get_image_element(self) -> WebElement:
        return self.root.find_element(*self.image_locator)

    def get_image_src(self) -> str:
        return self.get_image_element().get_attribute("src")

    def get_tag_elements(self):
        return self.root.find_elements(*self.tags_locator)

    def get_tags(self):
        return [tag.text.strip() for tag in self.get_tag_elements()]

    def get_title_element(self) -> WebElement:
        return self.root.find_element(*self.title_locator)

    def get_title(self) -> str:
        return self.get_title_element().text.strip()

    def get_creation_date_element(self) -> WebElement:
        return self.root.find_element(*self.creation_date_locator)

    def get_creation_date(self) -> str:
        return self.get_creation_date_element().text.strip()

    def get_author_name_element(self) -> WebElement:
        return self.root.find_element(*self.author_name_locator)

    def get_author_name(self) -> str:
        return self.get_author_name_element().text.strip()

    def click(self) -> NewsDetailsPage:
        self.root.find_element(*self.news_container_locator).click()
        return NewsDetailsPage(self.driver, self.news_id)