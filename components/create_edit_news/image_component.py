import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable, ElementNotFoundException


class ImageComponent(BaseComponent):
    """Component for handling image uploading, cropping, and previewing."""

    upload_input: WebElement
    drop_zone: WebElement
    drop_zone_text_element: WebElement
    browse_link: WebElement
    uploaded_image: WebElement
    preview_image: WebElement
    image_message: WebElement
    cropper: WebElement
    cancel_cropper_btn: WebElement
    submit_cropper_btn: WebElement

    locators: LocatorsTable = {
        "upload_input": (By.CSS_SELECTOR, "input[type='file']"),
        "drop_zone": (By.CSS_SELECTOR, "div.dropzone"),
        "drop_zone_text_element": (By.CSS_SELECTOR, "div.centered"),
        "browse_link": (By.CSS_SELECTOR, "div.centered label span"),
        "uploaded_image": (By.CSS_SELECTOR, "img.ngx-ic-source-image"),
        "preview_image": (By.CSS_SELECTOR, "div.image-preview img"),
        "image_message": (By.CSS_SELECTOR, "div.image-block p.warning"),
        "cropper": (By.CSS_SELECTOR, "image-cropper.cropper"),
        "cancel_cropper_btn": (By.CSS_SELECTOR, "div.cropper-buttons button.secondary-global-button"),
        "submit_cropper_btn": (By.CSS_SELECTOR, "div.cropper-buttons button.primary-global-button")
    }

    @allure.step("Check if Cancel button in image cropper is visible")
    def is_cancel_cropper_button_visible(self) -> bool:
        """Checks if the cancel button within the cropper tool is displayed."""
        return self.cancel_cropper_btn.is_displayed()

    @allure.step("Check if Submit button in image cropper is visible")
    def is_submit_cropper_button_visible(self) -> bool:
        """Checks if the submit button within the cropper tool is displayed."""
        return self.submit_cropper_btn.is_displayed()

    @allure.step("Get image upload error message text")
    def get_image_error(self) -> str:
        """Returns the text of the error message related to image uploading."""
        return self.image_message.text.strip()

    @allure.step("Upload image from file absolute path: {file_absolute_path}")
    def upload_image(self, file_absolute_path: str):
        """Uploads an image file by sending the file path to the hidden file input."""
        self.upload_input.send_keys(file_absolute_path)
        return self

    @allure.step("Get image input field value")
    def get_image_input_info(self) -> str:
        """Returns the 'value' attribute of the file input element."""
        return self.upload_input.get_attribute("value")

    @allure.step("Check if drop zone is visible")
    def is_image_field_visible(self) -> bool:
        """Checks if the drag-and-drop area for images is displayed."""
        return self.drop_zone.is_displayed()

    @allure.step("Check if uploaded image is visible")
    def is_image_visible(self) -> bool:
        """Checks if the main uploaded image is displayed in the cropper or preview."""
        return self.uploaded_image.is_displayed()

    @allure.step("Check if preview image is visible")
    def is_preview_image_visible(self) -> bool:
        """Checks if the final cropped preview image is displayed."""
        return self.preview_image.is_displayed()

    @allure.step("Get source URL of the uploaded image")
    def get_uploaded_image_src(self) -> str:
        """Returns the 'src' attribute of the uploaded image element."""
        return self.uploaded_image.get_attribute("src")

    @allure.step("Get source URL of the preview image")
    def get_preview_image_src(self) -> str:
        """Returns the 'src' attribute of the preview image element."""
        return self.preview_image.get_attribute("src")

    def _has_image_src_prefix(self, element: WebElement, prefix: str) -> bool:
        """Internal helper to check if an image source starts with a specific prefix."""
        src = element.get_attribute("src")
        return src is not None and src.startswith(prefix)

    @allure.step("Check if placeholder (data:image) is displayed")
    def is_placeholder_image_present(self) -> bool:
        """Checks if the displayed image is a base64 placeholder."""
        return self._has_image_src_prefix(self.uploaded_image, "data:image")

    @allure.step("Check if uploaded image (blob:) is displayed")
    def is_uploaded_image_present(self) -> bool:
        """Checks if the displayed image is a blob URL (indicating a successful local upload)."""
        return self._has_image_src_prefix(self.uploaded_image, "blob:")

    @allure.step("Click Submit crop")
    def submit_crop(self):
        """Clicks the submit button to confirm the image crop area."""
        self.submit_cropper_btn.click()
        return self

    @allure.step("Click Cancel crop")
    def cancel_crop(self):
        """Clicks the cancel button to exit the image cropper."""
        self.cancel_cropper_btn.click()
        return self

    @allure.step("Get text in drop zone")
    def get_drop_zone_text(self) -> str:
        """Returns the text within the drop zone, excluding the 'Browse' link text."""
        full_text = self.drop_zone.text
        browse_text = self.get_browse_text()
        return full_text.replace(browse_text, "").strip()

    @allure.step("Get 'Browse' link text")
    def get_browse_text(self) -> str:
        """Returns the text of the 'Browse' link element."""
        return self.browse_link.text.strip()

    @allure.step("Change image: upload new file {file_path} and submit crop")
    def change_image(self, file_path: str):
        """Full flow: cancels current crop, uploads new file, and submits the crop."""
        self.cancel_crop()
        self.upload_image(file_path)
        self.cropper.is_displayed()
        self.submit_crop()
        self.preview_image.is_displayed()
        return self

    @allure.step("Check if image error message is displayed")
    def is_image_error_msg_present(self) -> bool:
        """Checks if the error message has the specific warning CSS class."""
        class_attr = self.image_message.get_attribute("class")
        return "warning-color" in class_attr if class_attr else False

    @allure.step("Check if image preview is present")
    def is_preview_image_present(self) -> bool:
        """Safely checks if the preview image element exists and is displayed."""
        try:
            return self.preview_image.is_displayed()
        except ElementNotFoundException:
            return False
