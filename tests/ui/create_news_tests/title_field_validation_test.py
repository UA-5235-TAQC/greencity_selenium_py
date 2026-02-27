from typing import List

from components.tag_component import TagItem
from data.config import Config
from enums.language import Language
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

def login_user(driver):
    home_page = HomePage(driver).open()
    sign_in_modal = home_page.header.click_sign_in_link()
    sign_in_modal.sign_in()
    home_page.header.change_to_en()

def test_title_field_validation(get_driver):
    login_user(get_driver)

    create_news_page = CreateNewsPage(get_driver)
    create_news_page.open()
    assert create_news_page.get_current_url() == f"{Config.BASE_UI_GREEN_CITY_URL}/news/create-news"

    create_news_page.enter_title("")
    assert create_news_page.is_title_invalid() is True
    assert create_news_page.get_title_characters_count() == 0

    create_news_page.enter_title("A" * 171)
    assert create_news_page.is_title_invalid() is True
    assert create_news_page.get_title_characters_count() == 171

    create_news_page.enter_title(NEWS_TITLE)
    assert create_news_page.is_title_invalid() is False
    assert create_news_page.get_title_characters_count() == len(NEWS_TITLE)

    assert create_news_page.is_publish_button_enabled() is False

    # create_news_page.select_tags(TAGS_TO_SELECT)
    create_news_page.select_tag(EcoNewsTag.NEWS.en)
    create_news_page.content_component.enter_content(NEWS_CONTENT)
    assert create_news_page.is_publish_button_enabled() is True
