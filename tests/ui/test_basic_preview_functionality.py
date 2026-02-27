import pytest

from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.news_preview_page import NewsPreviewPage
from pages.news_page import NewsPage
from utils.date_utils import DateUtils
from data.config import Config
import allure

@allure.epic("UI Tests")
@allure.feature("News Creation")
@allure.story("News Preview Functionality")
@pytest.mark.usefixtures("sign_in")
class TestNewsDetails:

    @allure.title("Verify news preview content and navigation back to edit")
    @allure.description("""
        Test goals:
        1. Navigate to 'Create News' page.
        2. Fill title and content.
        3. Verify preview page data (title, text, date, author).
        4. Verify navigation back to the creation page.
    """)
    @allure.testcase("https://github.com/UA-5235-TAQC/greencity_selenium5235/issues/10")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_preview_check(self, get_driver):
        create_news_page = CreateNewsPage(get_driver)
        news_page = NewsPage(get_driver)
        news_preview_page = NewsPreviewPage(get_driver)

        news_page.open()
        assert "news" in get_driver.current_url, "URL should contain 'news' after opening news page"
        news_page.click_create_news()
        assert "create-news" in get_driver.current_url, "URL should contain 'create-news' after clicking 'Create news' button"
        create_news_page.enter_title("Test Preview")
        create_news_page.content_component.enter_content("This is a test preview content")
        create_news_page.click_preview_button()
        assert "preview" in get_driver.current_url, "URL should contain 'preview' after clicking preview button"
        assert news_preview_page.is_page_opened(), "News preview page should be opened after clicking preview button"
        assert news_preview_page.get_news_title() == "Test Preview", "News title in preview should match the entered title"
        assert news_preview_page.get_news_text() == "This is a test preview content", "News text in preview should match the entered content"
        assert news_preview_page.get_news_creating_date() == DateUtils.get_current_date_formatted(), "Creating date should be current date"
        assert news_preview_page.get_author_name() == Config.USER_NAME, "Author name should match the signed in user"
        news_preview_page.click_back_to_create_news_btn()
        assert "create-news" in get_driver.current_url, "URL should contain 'create-news' after clicking 'Back to create news' button"
        assert create_news_page.is_page_opened(), "Create news page should be opened after clicking 'Back to create news' button"

    