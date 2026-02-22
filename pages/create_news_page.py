import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.create_edit_news_page import CreateEditNewsPage


class CreateNewsPage(CreateEditNewsPage):
    _publish_btn = (By.XPATH, "//button[@type='submit' and contains(@class,'primary-global-button')]")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Open Create News page")
    def open(self):
        super().open()
        return self

    @allure.step("Check if Publish button is visible")
    def is_publish_button_visible(self) -> bool:
        elements = self.driver.find_elements(*self._publish_btn)
        return len(elements) > 0 and elements[0].is_displayed()

    @allure.step("Check if Publish button is enabled")
    def is_publish_button_enabled(self) -> bool:
        return self.driver.find_element(*self._publish_btn).is_enabled()

    @allure.step("Click Publish button")
    def click_publish(self):
        element = self.wait.until(EC.element_to_be_clickable(self._publish_btn))
        element.click()

    @allure.step("Get Publish button text")
    def get_publish_button_text(self) -> str:
        element = self.wait.until(EC.visibility_of_element_located(self._publish_btn))
        return element.text.strip()

    @allure.step("Reload CreateNewsPage")
    def reload(self):
        super().reload()
        return self

    @allure.step("Clear source text")
    def clear_source_field(self):
        super().clear_source_field()
        return self

    @allure.step("Enter news source URL: {url}")
    def enter_source(self, url):
        super().enter_source(url)
        return self

    @allure.step("Fill out and create news with mandatory fields: title, tags, content")
    def create_news(self, title, tags, content, source=None, image_path=None):

        self.enter_title(title)
        self.select_tags(tags)
        self.get_content_component().enter_content(content)

        if source:
            self.enter_source(source)

        if image_path:
            self.get_image_component().upload_image(image_path).submit_crop()

        return self
