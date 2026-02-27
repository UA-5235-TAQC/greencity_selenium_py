from selenium.webdriver.common.by import By
import allure
from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage
from utils.page_factory import LocatorsTable, ElementNotFoundException
from selenium.webdriver.remote.webelement import WebElement


class CreateNewsPage(CreateEditNewsPage):
    """Page object for Create News page."""

    publish_btn: WebElement

    locators: LocatorsTable = {
        "publish_btn": (By.XPATH,
                        "//button[@type='submit' and contains(@class,'primary-global-button')]")
    }

    @allure.step("Check if Publish button is visible")
    def is_publish_button_visible(self) -> bool:
        """Checks if the Publish button is displayed on the page."""
        try:
            return self.publish_btn.is_displayed()
        except ElementNotFoundException:
            return False

    @allure.step("Check if Publish button is enabled")
    def is_publish_button_enabled(self) -> bool:
        """Checks if the Publish button is clickable (enabled)."""
        return self.publish_btn.is_enabled()

    @allure.step("Click Publish button")
    def click_publish(self):
        """Performs a click action on the Publish button."""
        self.publish_btn.click()

    @allure.step("Get Publish button text")
    def get_publish_button_text(self) -> str:
        """Returns the trimmed text of the Publish button."""
        return self.publish_btn.text.strip()

    @allure.step("Fill out and create news with mandatory fields: title, tags, content")
    def create_news(self, title: str, tags: list[str], content: str, source: str = None, image_path: str = None):
        """
        Comprehensive method to fill all news details and prepare for publishing.
        Uses inherited methods and components (content_root, image_root).
        """
        self.enter_title(title)
        self.select_tags(tags)

        self.content_component.enter_content(content)

        if source:
            self.enter_source(source)

        if image_path:
            self.image_component.upload_image(image_path).submit_crop()

        return self
