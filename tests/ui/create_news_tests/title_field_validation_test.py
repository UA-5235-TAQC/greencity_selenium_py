import allure
from typing import List

from data.config import Config
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.home_page import HomePage

NEWS_TITLE: str = "Test News"
NEWS_CONTENT: str = "Description for test news Description for test news"
TAGS_TO_SELECT: List[str] = [
    EcoNewsTag.NEWS.ua,
    EcoNewsTag.ADS.ua,
    EcoNewsTag.EVENTS.ua,
]

@allure.feature("Create News")
@allure.story("Title field validation")
def test_title_field_validation(get_driver, logged_in_user):
    with allure.step("Login and open create news page"):
        create_news_page = CreateNewsPage(get_driver)
        create_news_page.open().header.change_to_en()
        assert create_news_page.get_current_url() == f"{Config.BASE_UI_GREEN_CITY_URL}/news/create-news"

    with allure.step("Validate empty title"):
        create_news_page.enter_title("")
        assert create_news_page.is_title_invalid()
        assert create_news_page.get_title_characters_count() == 0

    with allure.step("Validate too long title"):
        create_news_page.enter_title("A" * 171)
        assert create_news_page.is_title_invalid()
        assert create_news_page.get_title_characters_count() == 171

    with allure.step("Validate correct title"):
        create_news_page.enter_title(NEWS_TITLE)
        assert not create_news_page.is_title_invalid()
        assert create_news_page.get_title_characters_count() == len(NEWS_TITLE)
        assert not create_news_page.is_publish_button_enabled()

    with allure.step("Fill content and select tag"):
        create_news_page.select_tag(EcoNewsTag.NEWS.en)
        create_news_page.content_component.enter_content(NEWS_CONTENT)
        assert create_news_page.is_publish_button_enabled()