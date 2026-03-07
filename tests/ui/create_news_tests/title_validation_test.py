from typing import List
import allure
from allure_commons.types import Severity
from data.config import Config
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage

NEWS_TITLE: str = "Test News"
NEWS_CONTENT: str = "Description for test news Description for test news"
TAGS_TO_SELECT: List[str] = [
    EcoNewsTag.NEWS.ua,
    EcoNewsTag.ADS.ua,
    EcoNewsTag.EVENTS.ua,
]


@allure.epic("EcoNews UI")
@allure.feature("Create EcoNews")
@allure.story("Title field validation")
@allure.title("Verify Title field validation during news creation")
@allure.tag("Create News")
@allure.severity(Severity.NORMAL)
def test_title_field_validation(driver_with_login):
    """
    Test the Title field validation on the Create EcoNews page.

    Scenarios:
    1. Empty title should be invalid.
    2. Title exceeding 170 characters should be invalid.
    3. Correct title length should be valid, but Publish remains disabled until content and tag are filled.
    4. Publish button becomes enabled after filling content and selecting a tag.
    """
    with allure.step("Login and open create news page"):
        create_news_page = CreateNewsPage(driver_with_login)
        create_news_page.open().header.change_to_en()
        assert create_news_page.get_current_url() == f"{Config.BASE_UI_GREEN_CITY_URL}/news/create-news"

    with allure.step("Validate empty title"):
        create_news_page.enter_title("")
        assert create_news_page.is_title_invalid()
        assert create_news_page.get_title_length() == 0

    with allure.step("Validate too long title"):
        create_news_page.enter_title("A" * 171)
        assert create_news_page.is_title_invalid()
        assert create_news_page.get_title_length() == 171

    with allure.step("Validate correct title"):
        create_news_page.enter_title(NEWS_TITLE)
        assert not create_news_page.is_title_invalid()
        assert create_news_page.get_title_length() == len(NEWS_TITLE)
        assert not create_news_page.is_publish_button_enabled()

    with allure.step("Fill content and select tag"):
        create_news_page.select_tag(EcoNewsTag.NEWS.en)
        create_news_page.content_component.enter_content(NEWS_CONTENT)
        assert create_news_page.is_publish_button_enabled()
