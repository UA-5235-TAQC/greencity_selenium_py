import allure
from allure_commons.types import Severity
from components.create_edit_news.image_component import ImageComponent
from pages.create_edit_news.create_news_page import CreateNewsPage
from data.ui_news_test_data import NewsTestData
import pytest_check as check


@allure.tag("Create News")
@allure.epic("EcoNews Management")
@allure.feature("Create News")
@allure.story("Image upload validation for oversized files")
@allure.severity(Severity.NORMAL)
@allure.issue("6")
class TestUploadImage:

    @allure.description("The test checks successful validation when uploading a valid PNG image")
    def test_img_upload_positive(self, create_news_page: CreateNewsPage):
        """ Verifying that a valid PNG image is being uploaded. """
        image_component: ImageComponent = create_news_page.image_component
        image_component.upload_image(NewsTestData.SMALL_PNG_IMAGE)

        assert not image_component.is_image_error_msg_present(), "Error message should not be shown for valid PNG"
        assert image_component.is_image_visible(), "Image should be visible"
        assert image_component.get_uploaded_image_src() != "", "Image upload field should not be empty"
        assert image_component.is_uploaded_image_present(), "Loaded image should be present"
        assert image_component.is_cancel_cropper_button_visible(), "Cancel button on cropper should be visible"
        assert image_component.is_submit_cropper_button_visible(), "Submit button on cropper should be visible"

        check.equal(
            image_component.get_image_error(),
            "Upload only PNG or JPG. File size must be less than 10MB",
            "Error message should match"
        )
        check.equal(
            image_component.get_cancel_cropper_text(),
            "Cancel",
            "Cancel cropper button text should match"
        )
        check.equal(
            image_component.get_submit_cropper_text(),
            "Submit",
            "Submit cropper button text should match"
        )

    @allure.issue("6")
    @allure.description("The test checks validation error when uploading a GIF image (unsupported format)")
    def test_img_upload_gif_negative(self, create_news_page: CreateNewsPage):
        """ Checking GIF upload (unsupported format). """
        image_component: ImageComponent = create_news_page.image_component
        image_component.upload_image(NewsTestData.GIF_IMAGE)

        assert image_component.is_image_error_msg_present(), "Error message should be shown for unsupported GIF"
        check.is_false(image_component.is_preview_image()), "Preview image should not be visible for unsupported GIF"
