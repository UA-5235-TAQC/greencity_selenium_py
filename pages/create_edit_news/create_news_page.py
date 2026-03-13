from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
from pages.create_edit_news.create_edit_news_page import CreateEditNewsPage
from utils.page_factory import (LocatorsTable, ElementNotFoundException)


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

    def _click_publish_button(self) -> None:
        """Wait for and click the Publish button."""
        self.wait_for(EC.element_to_be_clickable(self.publish_btn))
        self.publish_btn.click()

    @allure.step("Click Publish button")
    def click_publish(self) -> "NewsPage":
        """Click the Publish button and open the Eco News page."""
        self._click_publish_button()

        from pages.news_page import NewsPage  # pylint: disable=import-outside-toplevel
        return NewsPage(self.driver).wait_until_opened()

    @allure.step("Click Publish button and open UBS page")
    def click_publish_ubs(self) -> "UbsCourierPage":
        """Click the Publish button and open the UBS Courier page."""
        self._click_publish_button()

        from pages.ubs_courier_page import UbsCourierPage  # pylint: disable=import-outside-toplevel
        return UbsCourierPage(self.driver).wait_until_opened()

    @allure.step("Get Publish button text")
    def get_publish_button_text(self) -> str:
        """Returns the trimmed text of the Publish button."""
        return self.publish_btn.text.strip()

    @allure.step("Fill out and create news with mandatory fields: title, tags, content")
    def create_news(  # pylint: disable=too-many-positional-arguments
            self, title: str, tags: list[str], content: str, source: str = None,
            image_path: str = None):
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
