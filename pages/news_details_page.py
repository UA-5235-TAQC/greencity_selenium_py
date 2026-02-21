from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from data.config import Config
import allure
from typing import List
#from pages.edit_news_page import EditNewsPage

class NewsDetailsPage(BasePage):
    root = (By.CSS_SELECTOR, "main-content app-container")
    back_to_news_button = (By.CSS_SELECTOR, ".button-link")
    delete_button = (By.CSS_SELECTOR, ".secondary-global-button.delete-news-button")
    edit_button = (By.XPATH, "//a[div[@class='edit-news']]")
    like_button = (By.CSS_SELECTOR, "img.news_like")
    likes_count = (By.CSS_SELECTOR, ".like_wr .numerosity_likes")
    social_links = (By.CSS_SELECTOR, ".news-links-images img")
    tags = (By.CSS_SELECTOR, ".tags .tags-item")
    comments_container = (By.XPATH, "(//app-comments-container)[1]")
    comments_form = (By.CSS_SELECTOR, ".app-add-comment form")
    recommended_news = (By.CSS_SELECTOR, ".app-eco-news-widget")
    news_title_text = (By.CSS_SELECTOR, ".news-title-container .news-title")
    post_date = (By.CSS_SELECTOR, ".news-info-date")
    author_name = (By.CSS_SELECTOR, ".news-info-author")
    content = (By.CSS_SELECTOR, ".ql-editor")
    news_image = (By.CSS_SELECTOR, "img.news-image-img")

    def __init__(self, driver, news_id: int):
        super().__init__(driver)
        self.news_id = news_id

    @allure.step("Open news details page with ID")
    def open(self):
        url = f"{Config.BASE_UI_GREEN_CITY_URL}/news/{self.news_id}"
        self.driver.get(url)
        return self
    
    @allure.step("Click 'Back to news' button")
    def click_back_to_news_button(self):
        self.driver.find_element(*self.back_to_news_button).click()

    @allure.step("Click 'Delete news' button")
    def click_delete_button(self):
        self.driver.find_element(*self.delete_button).click()
        return self

    #@allure.step("Click 'Edit news' button")
    #def click_edit_button(self):
    #    self.driver.find_element(*self.edit_button).click()
    #    return EditNewsPage(self.driver, self.news_id)

    @allure.step("Check if Edit button is enabled")
    def is_edit_button_enabled(self) -> bool:
        return self.driver.find_element(*self.edit_button).is_enabled()

    @allure.step("Click 'Like' button")
    def click_like_button(self):
        self.driver.find_element(*self.like_button).click()
        return self

    @allure.step("Remove like from the news if it is active")
    def delete_like(self):
        if self.is_like_active():
            initial_count = self.get_likes_count()
            self.click_like_button()
            self.wait_for_likes_to_change(initial_count - 1)
        return self
    
    @allure.step("Wait until likes count changes to expected value: {expected_count}")
    def wait_for_likes_to_change(self, expected_count: int):
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, 5).until(lambda d: self.get_likes_count() == expected_count)
    
    @allure.step("Check if like is active on the page")
    def is_like_active(self) -> bool:
        src = self.driver.find_element(*self.like_button).get_attribute("src")
        return src is not None and "liked.png" in src

    @allure.step("Get likes count")
    def get_likes_count(self) -> int:
        text = self.driver.find_element(*self.likes_count).text
        return int(text.strip()) if text.strip() else 0

    @allure.step("Get news tags")
    def get_tags(self) -> List[str]:
        elements = self.driver.find_elements(*self.tags)
        return [el.text for el in elements]

    @allure.step("Get title text")
    def get_title_value(self) -> str:
        return self.driver.find_element(*self.news_title_text).text.strip()

    @allure.step("Get post date")
    def get_post_date(self) -> str:
        return self.driver.find_element(*self.post_date).text.strip()

    @allure.step("Get author name")
    def get_author(self) -> str:
        text = self.driver.find_element(*self.author_name).text
        return text[3:].strip()

    @allure.step("Get news ID")
    def get_id(self) -> int:
        return self.news_id

    @allure.step("Get content text")
    def get_content_text(self) -> str:
        return self.driver.find_element(*self.content).text

    @allure.step("Get news image src")
    def get_news_image_src(self) -> str:
        return self.driver.find_element(*self.news_image).get_attribute("src")