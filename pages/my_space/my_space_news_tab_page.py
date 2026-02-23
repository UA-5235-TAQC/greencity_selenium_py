import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pages.my_space.my_space_base_page import MySpaceBasePage

class MySpaceNewsTabPage(MySpaceBasePage):

    _PAGE_TITLE = (By.CSS_SELECTOR, ".header app-set-count")
    _NEWS_LIST = (By.CSS_SELECTOR, "ul.news-list > li")
    _TAGS = (By.CSS_SELECTOR, ".tag-button .text")
    _ADD_NEWS_BUTTON = (By.ID, "create-button-news")
    _NEWS_COUNT_LABEL = (By.CSS_SELECTOR, ".header app-set-count span.ng-star-inserted")
    _FAVOURITES_BUTTON = (By.CSS_SELECTOR, ".buttons-wrapper .favourites")

    def get_page_title(self) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self._PAGE_TITLE))
        return el.text.split("\n")[0].strip()

    def get_news_list(self):
        return self.driver.find_elements(*self._NEWS_LIST)

    def get_all_tags(self):
        tags = self.driver.find_elements(*self._TAGS)
        return [t.text.strip() for t in tags if t.text.strip()]

    def filter_by_tag(self, tag: str):
        for t in self.driver.find_elements(*self._TAGS):
            self.wait.until(EC.visibility_of(t))
            if t.text.strip() == tag:
                t.click()
                return self
        raise NoSuchElementException(f"Tag '{tag}' not found")

    def click_add_news(self):
        self.wait.until(EC.element_to_be_clickable(self._ADD_NEWS_BUTTON)).click()
        return self

    def get_news_count(self) -> int:
        text = self.wait.until(EC.visibility_of_element_located(self._NEWS_COUNT_LABEL)).text
        digits = re.sub(r"\D+", "", text)
        return int(digits) if digits else 0

    def click_favourites(self):
        self.wait.until(EC.element_to_be_clickable(self._FAVOURITES_BUTTON)).click()
        return self