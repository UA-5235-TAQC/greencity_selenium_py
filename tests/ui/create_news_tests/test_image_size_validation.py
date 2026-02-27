import allure
import pytest
import os

from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_page import NewsPage


@allure.epic("UI Tests")
@allure.feature("News Creation")
@allure.story("News Preview Functionality")
@pytest.mark.usefixtures("sign_in")
class TestNewsImageSizeValidation:

    def test_image_size_validation(self, get_driver):
        create_news_page = CreateNewsPage(get_driver)
        news_page = NewsPage(get_driver)
        project_root_path = os.getcwd()
        relative_path_to_image = "tests/resources/images/Andromeda_Galaxy.jpg"
        absolute_path = os.path.join(project_root_path, relative_path_to_image)

        news_page.open()
        assert "news" in get_driver.current_url, "URL should contain 'news' after opening news page"
        news_page.click_create_news()
        assert "create-news" in get_driver.current_url, "URL should contain 'create-news' after clicking 'Create news' button"
        create_news_page.image_component.upload_image(absolute_path)
        assert create_news_page.image_component.get_image_error() == \
            "Upload only PNG or JPG. File size must be less than 10MB" or \
            "Завантажуйте лише PNG або JPEG. Розмір файлу не повинен перевищувати 10Mb"
        assert not create_news_page.image_component.is_uploaded_image_present(), "Image source should be empty for invalid image upload"