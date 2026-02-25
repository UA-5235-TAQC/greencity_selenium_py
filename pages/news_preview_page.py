import allure
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from utils.page_factory import LocatorsTable, By
from pages.base_page import BasePage


class NewsPreviewPage(BasePage):

    back_to_create_news_btn: WebElement
    public_news_btn: WebElement
    news_title: WebElement
    tags_root: WebElement
    news_creating_date: WebElement
    author_name: WebElement
    news_image: WebElement
    news_text: WebElement
    news_source: WebElement
    root: WebElement

    locators: LocatorsTable = {
        "back_to_create_news_btn": (By.CSS_SELECTOR, ".button-link"),
        "public_news_btn": (By.CSS_SELECTOR, ".submit-form"),
        "news_title": (By.CSS_SELECTOR, ".news-title"),
        "tags_root": (By.CSS_SELECTOR, ".tags"),
        "news_creating_date": (By.CSS_SELECTOR, ".news-info-date"),
        "author_name": (By.CSS_SELECTOR, ".news-info-author"),
        "news_image": (By.CSS_SELECTOR, ".news-image-img"),
        "news_text": (By.CSS_SELECTOR, ".news-text-content p"),
        "news_source": (By.CSS_SELECTOR, ".source-text"),
        "root": (By.CSS_SELECTOR, ".main-content.app-container"),
    }

    # ---------- page state ----------

    @allure.step("Check preview page is opened")
    def is_page_opened(self) -> bool:
        return self.news_title.is_displayed()

    @allure.step("Wait until preview page is opened")
    def wait_until_opened(self):
        _ = self.news_title
        return self

    # ---------- actions ----------

    @allure.step("Click 'Public news' button")
    def click_public_news_btn(self):
        self.public_news_btn.click()

    @allure.step("Click 'Back to create news'")
    def click_back_to_create_news_btn(self):
        from pages.create_news_page import CreateNewsPage
        self.back_to_create_news_btn.click()
        return CreateNewsPage(self.driver)

    @allure.step("Back to editing news with id: {news_id}")
    def back_to_editing(self, news_id: int):
        from pages.edit_news_page import EditNewsPage
        self.back_to_create_news_btn.click()
        return EditNewsPage(self.driver, news_id)

    # ---------- getters ----------

    @allure.step("Get news title")
    def get_news_title(self) -> str:
        return self.news_title.text

    @allure.step("Get news creating date")
    def get_news_creating_date(self) -> str:
        return self.news_creating_date.text

    @allure.step("Get author name")
    def get_author_name(self) -> str:
        text = self.author_name.text
        return text.split(" ", 1)[1]

    @allure.step("Get news text")
    def get_news_text(self) -> str:
        return self.news_text.text

    @allure.step("Get news source")
    def get_news_source(self) -> str:
        return self.news_source.text

    # ---------- tags ----------

    @allure.step("Get tag elements")
    def get_tag_elements(self) -> List[WebElement]:
        return self.tags_root.find_elements(By.CLASS_NAME, "tags-item")

    @allure.step("Get tag texts")
    def get_tag_texts(self) -> List[str]:
        return [tag.text.strip() for tag in self.get_tag_elements()]

    # ---------- image ----------

    @allure.step("Check image visible")
    def is_image_visible(self) -> bool:
        parent = self.news_image.find_element(By.XPATH, "..")
        return parent.is_displayed()

    @allure.step("Get preview image src")
    def get_preview_image_src(self) -> str:
        return self.news_image.get_attribute("src")