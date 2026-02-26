from typing import List
import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.my_space.my_space_base_page import MySpaceBasePage
from utils.page_factory import LocatorsTable
from utils.web_element_utils import get_int_from_text

class MySpaceNewsTabPage(MySpaceBasePage):

    page_title: WebElement
    add_news_button: WebElement
    favourites_button: WebElement
    news_count_label: WebElement
    news_items: List[WebElement]
    tags: List[WebElement]

    locators: LocatorsTable = {
        "page_title": (By.CSS_SELECTOR, ".header app-set-count"),
        "add_news_button": (By.ID, "create-button-news"),
        "favourites_button": (By.CSS_SELECTOR, ".buttons-wrapper .favourites"),
        "news_count_label": (By.CSS_SELECTOR, ".header app-set-count span.ng-star-inserted"),
        "news_items": (By.CSS_SELECTOR, "ul.news-list > li"),
        "tags": (By.CSS_SELECTOR, "button.tag-button"),
    }

    @allure.step("Get page title")
    def get_page_title(self) -> str:
        return self.page_title.text.split("\n")[0].strip()

    @allure.step("Get news list")
    def get_news_list(self) -> List[WebElement]:
        return self.news_items

    @allure.step("Get all tags")
    def get_all_tags(self) -> List[str]:
        tags_list = []
        for tag in self.tags:
            text = tag.text.strip()
            if text:
                tags_list.append(text)
        return tags_list

    @allure.step("Filter by tag: {tag}")
    def filter_by_tag(self, tag: str):
        for t in self.tags:
            if t.text.strip() == tag:
                t.click()
                return self
        raise ValueError(f"Tag '{tag}' not found")

    @allure.step("Click Add News button")
    def click_add_news(self):
        self.add_news_button.click()
        return self

    @allure.step("Get news count")
    def get_news_count(self) -> int:
        return get_int_from_text(self.news_count_label)

    @allure.step("Click Favourites button")
    def click_favourites(self):
        self.favourites_button.click()
        return self