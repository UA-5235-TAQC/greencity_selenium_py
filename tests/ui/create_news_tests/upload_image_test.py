import allure
from allure_commons.types import Severity
import pytest
from components.create_edit_news.image_component import ImageComponent
from data.ui_news_test_data import TOO_LARGE_IMAGE, SMALL_PNG_IMAGE, GIF_IMAGE
from pages.create_edit_news.create_news_page import CreateNewsPage
import pytest_check as check
from pages.news_page import NewsPage


@allure.epic("EcoNews UI")
@allure.feature("Create News")
@allure.tag("Create News")
@allure.severity(Severity.NORMAL)
class TestUploadImage:
    """
    Test suite for verifying image upload behavior in the Create News page.

    Includes tests for:
    - Uploading an image larger than 10MB (should fail)
    - Uploading a valid PNG image (should succeed)
    - Uploading an unsupported GIF image (should fail)
    """

    @allure.story("Image Size Validation")
    @allure.title("Validation of error message when uploading an image larger than 10MB")
    @pytest.mark.usefixtures("driver_with_login")
    def test_image_size_validation(self, get_driver):
        """
        Verify that uploading an image larger than 10MB displays a validation error
        and the image is not loaded.
        """
        create_news_page = CreateNewsPage(get_driver)
        news_page = NewsPage(get_driver)

        news_page.open()
        assert "news" in get_driver.current_url, "URL should contain 'news' after opening news page"
        news_page.click_create_news()
        assert "create-news" in get_driver.current_url, "URL should contain 'create-news' after clicking 'Create news' button"
        create_news_page.image_component.upload_image(TOO_LARGE_IMAGE)
        assert create_news_page.image_component.get_image_error() == \
               "Upload only PNG or JPG. File size must be less than 10MB" or \
               "Завантажуйте лише PNG або JPEG. Розмір файлу не повинен перевищувати 10Mb"
        assert not create_news_page.image_component.is_uploaded_image_present(), "Image source should be empty for invalid image upload"

    @allure.issue("6")
    @allure.story("Image Size Validation")
    @allure.title("The test checks successful validation when uploading a valid PNG image")
    def test_img_upload_positive(self, create_news_page: CreateNewsPage):
        """Verify that a valid PNG image is being uploaded."""
        image_component: ImageComponent = create_news_page.image_component
        image_component.upload_image(SMALL_PNG_IMAGE)

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
    @allure.story("Check GIF upload (unsupported format)")
    @allure.title("The test checks validation error when uploading a GIF image (unsupported format)")
    def test_img_upload_gif_negative(self, create_news_page: CreateNewsPage):
        """Check GIF upload (unsupported format)."""
        image_component: ImageComponent = create_news_page.image_component
        image_component.upload_image(GIF_IMAGE)

        assert image_component.is_image_error_msg_present(), "Error message should be shown for unsupported GIF"
        check.is_false(image_component.is_preview_image()), "Preview image should not be visible for unsupported GIF"
