import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from components.tag_item import TagItem
from components.image_component import ImageComponent
from components.content_component import ContentComponent
from components.cancel_modal_component import CancelModalComponent
from pages.news_preview_page import NewsPreviewPage


class CreateEditNewsPage(BasePage):
    _root = (By.CSS_SELECTOR, "div.main-content")
    _title_input = (By.CSS_SELECTOR, "textarea[formcontrolname='title']")
    _page_title_header = (By.CSS_SELECTOR, "div.title h2.title-header")
    _tag_root_elements = (By.CSS_SELECTOR, "div.tags-box button.tag-button")
    _source_input = (By.CSS_SELECTOR, "input[formcontrolname='source']")
    _image_root = (By.CSS_SELECTOR, "div.image-block")
    _source_message = (By.CSS_SELECTOR, "div.source-block")
    _cancel_btn = (By.CSS_SELECTOR, ".submit-buttons button.tertiary-global-button")
    _preview_btn = (By.CSS_SELECTOR, ".submit-buttons button.secondary-global-button")
    _title_character_counter = (By.CSS_SELECTOR, ".title-block div span.field-info")
    _post_date = (By.CSS_SELECTOR, "div.date p:nth-of-type(1) span:last-child")
    _author_name = (By.CSS_SELECTOR, "div.date p:nth-of-type(2) span:last-child")
    _content_root = (By.CSS_SELECTOR, "div.textarea-wrapper")
    _cancel_modal_container = (By.CSS_SELECTOR, "mat-dialog-container app-warning-pop-up")

    def __init__(self, driver):
        super().__init__(driver)

    def _clear_element_by_keyboard(self, element):
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        return self

    @allure.step("Open Create News page")
    def open(self):
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/news/create-news")
        return self

    @allure.step("Check if Create/Edit News page is opened")
    def is_page_opened(self):
        elements = self.driver.find_elements(*self._title_input)
        return len(elements) > 0 and elements[0].is_displayed()

    @allure.step("Wait until Create/Edit News page is opened")
    def wait_until_opened(self):
        self.wait.until(EC.visibility_of_element_located(self._title_input))
        return self

    @allure.step("Enter news title: {title}")
    def enter_title(self, title):
        element = self.wait.until(EC.element_to_be_clickable(self._title_input))
        self._clear_element_by_keyboard(element)
        element.send_keys(title)
        return self

    @allure.step("Enter news source: {url}")
    def enter_source(self, url):
        element = self.driver.find_element(*self._source_input)
        self._clear_element_by_keyboard(element)
        element.send_keys(url)
        return self

    @allure.step("Clear source field")
    def clear_source_field(self):
        element = self.driver.find_element(*self._source_input)
        self._clear_element_by_keyboard(element)
        return self

    @allure.step("Get all tag items on page")
    def get_tag_items(self):
        elements = self.driver.find_elements(*self._tag_root_elements)
        return [TagItem(self.driver, el) for el in elements]

    def _get_tag_by_name(self, tag_name):
        for tag in self.get_tag_items():
            if tag.get_name().lower() == tag_name.lower():
                return tag
        raise NoSuchElementException(f"Tag not found: {tag_name}")

    @allure.step("Click tag by name: {tag_name}")
    def click_tag_by_name(self, tag_name):
        self._get_tag_by_name(tag_name).click()
        return self

    @allure.step("Select multiple tags: {tag_names}")
    def select_tags(self, tag_names):
        for name in tag_names:
            tag = self._get_tag_by_name(name)
            if not tag.is_selected():
                tag.click()
        return self

    @allure.step("Get list of selected tags")
    def get_selected_tags(self):
        return [tag.get_name() for tag in self.get_tag_items() if tag.is_selected()]

    def get_image_component(self):
        root = self.driver.find_element(*self._image_root)
        return ImageComponent(root, self.driver)

    def get_content_component(self):
        root = self.driver.find_element(*self._content_root)
        return ContentComponent(root, self.driver)

    def get_title_value(self):
        return self.driver.find_element(*self._title_input).get_attribute("value")

    def get_source_message_text(self):
        return self.driver.find_element(*self._source_message).text.strip()

    @allure.step("Click Preview button")
    def click_preview(self):
        self.driver.find_element(*self._preview_btn).click()
        return NewsPreviewPage(self.driver)

    @allure.step("Get Cancel modal component")
    def get_cancel_modal(self):
        container = self.wait.until(EC.visibility_of_element_located(self._cancel_modal_container))
        return CancelModalComponent(container, self.driver)

    @allure.step("Prepend text to title")
    def prepend_title(self, text):
        current = self.get_title_value()
        self.enter_title(text + (current if current else ""))
        return self

    def _remove_title_chars(self, count, from_start=False):
        current = self.get_title_value()
        if current:
            new_val = current[count:] if from_start else current[:-count]
            self.enter_title(new_val if len(current) > count else "")
        return self

    @allure.step("Remove last {count} characters from title")
    def remove_last_title_chars(self, count):
        return self._remove_title_chars(count, from_start=False)

    @allure.step("Reload page")
    def reload(self):
        self.driver.refresh()
        self.wait_until_opened()
        return self
