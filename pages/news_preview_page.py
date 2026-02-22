from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class NewsPreviewPage(BasePage):
    # locators
    BACK_TO_CREATE_NEWS_BTN = (By.CSS_SELECTOR, ".button-link")
    PUBLIC_NEWS_BTN = (By.CSS_SELECTOR, ".submit-form")
    NEWS_TITLE = (By.CSS_SELECTOR, ".news-title")
    TAGS_ROOT = (By.CSS_SELECTOR, ".tags")
    TAG_ITEMS = (By.CLASS_NAME, "tags-item")
    NEWS_CREATING_DATE = (By.CSS_SELECTOR, ".news-info-date")
    AUTHOR_NAME = (By.CSS_SELECTOR, ".news-info-author")
    NEWS_IMAGE = (By.CSS_SELECTOR, ".news-image-img")
    NEWS_TEXT = (By.CSS_SELECTOR, ".news-text-content p")
    NEWS_SOURCE = (By.CSS_SELECTOR, ".source-text")
    ROOT = (By.CSS_SELECTOR, ".main-content.app-container")

    def __init__(self, driver):
        super().__init__(driver)

    # ---------- page state ----------

    def is_page_opened(self) -> bool:
        return self.wait_until_visible(self.NEWS_TITLE).is_displayed()

    def wait_until_opened(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.NEWS_TITLE)
        )
        return self

    # ---------- actions ----------

    def click_public_news_btn(self):
        self.wait_until_clickable(self.PUBLIC_NEWS_BTN).click()

    def click_back_to_create_news_btn(self):
        from pages.create_news_page import CreateNewsPage
        self.wait_until_clickable(self.BACK_TO_CREATE_NEWS_BTN).click()
        return CreateNewsPage(self.driver)

    def back_to_editing(self, news_id: int):
        from pages.edit_news_page import EditNewsPage
        self.wait_until_clickable(self.BACK_TO_CREATE_NEWS_BTN).click()
        return EditNewsPage(self.driver, news_id)

    # ---------- getters ----------

    def get_news_title(self) -> str:
        return self.wait_until_visible(self.NEWS_TITLE).text

    def get_news_creating_date(self) -> str:
        return self.wait_until_visible(self.NEWS_CREATING_DATE).text

    def get_author_name(self) -> str:
        text = self.wait_until_visible(self.AUTHOR_NAME).text
        return text.split(" ", 1)[1]

    def get_news_text(self) -> str:
        return self.wait_until_visible(self.NEWS_TEXT).text

    def get_news_source(self) -> str:
        return self.wait_until_visible(self.NEWS_SOURCE).text

    # ---------- tags ----------

    def get_tag_elements(self):
        root = self.wait_until_visible(self.TAGS_ROOT)
        return root.find_elements(*self.TAG_ITEMS)

    def get_tag_texts(self):
        return [tag.text.strip() for tag in self.get_tag_elements()]

    # ---------- image ----------

    def get_news_image_element(self):
        return self.wait_until_visible(self.NEWS_IMAGE)

    def is_image_visible(self) -> bool:
        image = self.get_news_image_element()
        parent = image.find_element(By.XPATH, "..")
        return parent.is_displayed()

    def get_preview_image_src(self, timeout=5) -> str:
        wait = WebDriverWait(self.driver, timeout)

        def image_has_src(driver):
            src = driver.find_element(*self.NEWS_IMAGE).get_attribute("src")
            return src if src else False

        return wait.until(image_has_src)