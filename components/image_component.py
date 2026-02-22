import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.base_component import BaseComponent


class ImageComponent(BaseComponent):
    _upload_input = (By.CSS_SELECTOR, "input[type='file']")
    _drop_zone = (By.CSS_SELECTOR, "div.dropzone")
    _drop_zone_text = (By.CSS_SELECTOR, "div.centered")
    _browse_link = (By.CSS_SELECTOR, "div.centered label span")
    _uploaded_image = (By.CSS_SELECTOR, "img.ngx-ic-source-image")
    _preview_image = (By.CSS_SELECTOR, "div.image-preview img")
    _image_message = (By.CSS_SELECTOR, "div.image-block p.warning")
    _cropper = (By.CSS_SELECTOR, "image-cropper.cropper")
    _cancel_cropper_btn = (By.CSS_SELECTOR, "div.cropper-buttons button.secondary-global-button")
    _submit_cropper_btn = (By.CSS_SELECTOR, "div.cropper-buttons button.primary-global-button")

    def __init__(self, root, driver, timeout=None):
        super().__init__(root, driver, timeout)

    @allure.step("Check if Cancel button in image cropper is visible")
    def is_cancel_cropper_button_visible(self) -> bool:
        return self.root.find_element(*self._cancel_cropper_btn).is_displayed()

    @allure.step("Check if Submit button in image cropper is visible")
    def is_submit_cropper_button_visible(self) -> bool:
        return self.root.find_element(*self._submit_cropper_btn).is_displayed()

    @allure.step("Get image upload error message text")
    def get_image_error(self) -> str:
        return self.root.find_element(*self._image_message).text.strip()

    @allure.step("Upload image from file absolute path: {file_absolute_path}")
    def upload_image(self, file_absolute_path: str):
        self.root.find_element(*self._upload_input).send_keys(file_absolute_path)
        return self

    @allure.step("Get image input field value")
    def get_image_input_info(self) -> str:
        return self.root.find_element(*self._upload_input).get_attribute("value")

    @allure.step("Check if drop zone is visible")
    def is_image_field_visible(self) -> bool:
        return self.root.find_element(*self._drop_zone).is_displayed()

    @allure.step("Check if uploaded image is visible")
    def is_image_visible(self) -> bool:
        return self.root.find_element(*self._uploaded_image).is_displayed()

    @allure.step("Check if preview image is visible")
    def is_preview_image_visible(self) -> bool:
        return self.root.find_element(*self._preview_image).is_displayed()

    def _get_image_src(self, locator) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.get_attribute("src")

    @allure.step("Get source URL of the uploaded image")
    def get_uploaded_image_src(self) -> str:
        return self._get_image_src(self._uploaded_image)

    @allure.step("Get source URL of the preview image")
    def get_preview_image_src(self) -> str:
        return self._get_image_src(self._preview_image)

    def _has_image_src_prefix(self, locator, prefix: str) -> bool:
        src = self._get_image_src(locator)
        return src is not None and src.startswith(prefix)

    @allure.step("Check if placeholder (data:image) is displayed")
    def is_placeholder_image_present(self) -> bool:
        return self._has_image_src_prefix(self._uploaded_image, "data:image")

    @allure.step("Check if uploaded image (blob:) is displayed")
    def is_uploaded_image_present(self) -> bool:
        return self._has_image_src_prefix(self._uploaded_image, "blob:")

    @allure.step("Click Submit crop")
    def submit_crop(self):
        self.root.find_element(*self._submit_cropper_btn).click()
        return self

    @allure.step("Click Cancel crop")
    def cancel_crop(self):
        self.root.find_element(*self._cancel_cropper_btn).click()
        return self

    @allure.step("Get text in drop zone")
    def get_drop_zone_text(self) -> str:
        full_text = self.root.find_element(*self._drop_zone).text
        browse_text = self.get_browse_text()
        return full_text.replace(browse_text, "").strip()

    @allure.step("Get 'Browse' link text")
    def get_browse_text(self) -> str:
        return self.root.find_element(*self._browse_link).text.strip()

    @allure.step("Change image: upload new file and submit crop")
    def change_image(self, file_path: str):
        self.cancel_crop()
        self.upload_image(file_path)
        self.wait.until(EC.visibility_of_element_located(self._cropper))
        self.submit_crop()
        self.wait.until(EC.visibility_of_element_located(self._preview_image))
        return self

    @allure.step("Check if image error message is displayed")
    def is_image_error_msg_present(self) -> bool:
        class_attr = self.root.find_element(*self._image_message).get_attribute("class")
        return "warning-color" in class_attr if class_attr else False

    @allure.step("Check if image preview is present")
    def is_preview_image_present(self) -> bool:
        try:
            return self.root.find_element(*self._preview_image).is_displayed()
        except NoSuchElementException:
            return False
