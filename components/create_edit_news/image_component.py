import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class ImageComponent(BaseComponent):
    """ Component representing the news image component."""

    UPLOAD_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    PREVIEW_IMAGE = (By.CSS_SELECTOR, "div.image-preview img")
    CROPPER = (By.CSS_SELECTOR, "image-cropper.cropper")
    CANCEL_CROPPER_BTN = (By.CSS_SELECTOR, "div.cropper-buttons button.secondary-global-button")
    SUBMIT_CROPPER_BTN = (By.CSS_SELECTOR, "div.cropper-buttons button.primary-global-button")

    @allure.step("Upload image from file absolute path: {file_absolute_path}")
    def upload_image(self, file_absolute_path: str):
        """ Upload image from file absolute path. """
        self.find(*self.UPLOAD_INPUT).send_keys(file_absolute_path)
        return self

    @allure.step("Click Submit crop")
    def submit_crop(self):
        """ Click Submit crop. """
        self.click(*self.SUBMIT_CROPPER_BTN)
        return self

    @allure.step("Click Cancel crop")
    def cancel_crop(self):
        """ Click Cancel crop. """
        self.click(*self.CANCEL_CROPPER_BTN)
        return self

    @allure.step("Change image: upload new file and submit crop")
    def change_image(self, file_path: str):
        """ Change image: upload new file and submit crop. """
        self.cancel_crop()
        self.upload_image(file_path)
        self.wait_until_visible(self.CROPPER)
        self.submit_crop()
        self.wait_until_visible(self.PREVIEW_IMAGE)
        return self
