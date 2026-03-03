from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from utils.web_element_utils import enter_text


class CommentFormComponent(BaseComponent):
    """Component representing the Add Comment form."""

    comment_input: WebElement
    image_upload_btn: WebElement
    emoji_btn: WebElement
    submit_btn: WebElement

    locators: LocatorsTable = {
        "comment_input": (By.CSS_SELECTOR, "app-comment-textarea .comment-textarea"),
        "image_upload_btn": (By.CSS_SELECTOR, "button.image-upload-btn"),
        "emoji_btn": (By.CSS_SELECTOR, "button.emoji-picker-btn"),
        "submit_btn": (By.CSS_SELECTOR, "button.primary-global-button"),
    }

    @allure.step("Enter comment text: {text}")
    def enter_comment(self, text: str) -> None:
        """Type text into the comment textarea."""
        enter_text(self.comment_input, text)

    @allure.step("Submit comment")
    def submit_comment(self) -> None:
        """Click the Comment button."""
        self.submit_btn.click()

    @allure.step("Create comment with text: {text}")
    def add_comment(self, text: str) -> None:
        """Full flow: enter text and submit."""
        self.enter_comment(text)
        self.submit_comment()

    @allure.step("Check if submit button is enabled")
    def is_submit_enabled(self) -> bool:
        """Check if the Comment button is enabled."""
        return self.submit_btn.is_enabled()

    @allure.step("Click image upload button")
    def click_image_upload(self) -> None:
        """Click the image upload button."""
        self.image_upload_btn.click()

    @allure.step("Click emoji picker button")
    def click_emoji(self) -> None:
        """Click the emoji picker button."""
        self.emoji_btn.click()

    @allure.step("Check if emoji picker is visible")
    def is_emoji_visible(self) -> bool:
        """Check if emoji button is visible."""
        return self.emoji_btn.is_displayed()

    @allure.step("Check if image upload button is visible")
    def is_image_upload_visible(self) -> bool:
        """Check if image upload button is visible."""
        return self.image_upload_btn.is_displayed()
