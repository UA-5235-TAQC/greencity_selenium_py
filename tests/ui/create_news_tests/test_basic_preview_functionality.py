import pytest
import allure
from allure_commons.types import Severity
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.news_preview_page import NewsPreviewPage
from pages.news_page import NewsPage
from utils.date_utils import DateUtils
from data.config import Config


@allure.epic("EcoNews UI")
@allure.feature("Create EcoNews")
@allure.story("News Preview Functionality")
@allure.title("Verify news preview content and navigation back to edit")
@allure.description("""
    Test goals:
    1. Navigate to 'Create News' page.
    2. Fill title and content.
    3. Verify preview page data (title, text, date, author).
    4. Verify navigation back to the creation page.
""")
@allure.tag("Create News")
@allure.issue("10")
@allure.severity(Severity.NORMAL)
@pytest.mark.usefixtures("driver_with_login")
def test_news_preview_check(get_driver):
    """
    Verify that the News Preview page displays the correct title, content,
    author, and creation date, and allows navigation back to the Create News page.
    """
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
    assert create_news_page.is_page_opened_after_preview_click_back(), "Create news page should be opened after clicking 'Back to create news' button"
