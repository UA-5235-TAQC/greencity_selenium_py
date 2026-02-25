import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent
from selenium.webdriver.remote.webelement import WebElement
from utils.page_factory import LocatorsTable


class ImageComponent(BaseComponent):
    """ Component representing the news image component."""

    upload_input: WebElement
    preview_image: WebElement
    cropper: WebElement
    cancel_cropper_btn: WebElement
    submit_cropper_btn: WebElement

    locators: LocatorsTable = {
        "upload_input": (By.CSS_SELECTOR, "input[type='file']"),
        "preview_image": (By.CSS_SELECTOR, "div.image-preview img"),
        "cropper": (By.CSS_SELECTOR, "image-cropper.cropper"),
        "cancel_cropper_btn": (By.CSS_SELECTOR, "div.cropper-buttons button.secondary-global-button"),
        "submit_cropper_btn": (By.CSS_SELECTOR, "div.cropper-buttons button.primary-global-button")
    }

    @allure.step("Upload image from file absolute path: {file_absolute_path}")
    def upload_image(self, file_absolute_path: str):
        """ Upload image from file absolute path. """
        self.upload_input.send_keys(file_absolute_path)
        return self

    @allure.step("Click Submit crop")
    def submit_crop(self):
        """ Click Submit crop. """
        self.submit_cropper_btn.click()
        return self

    @allure.step("Click Cancel crop")
    def cancel_crop(self):
        """ Click Cancel crop. """
        self.cancel_cropper_btn.click()
        return self

    @allure.step("Change image: upload new file and submit crop")
    def change_image(self, file_path: str):
        """ Change image: upload new file and submit crop. """
        self.cancel_crop()
        self.upload_image(file_path)
        self.submit_crop()
        return self
