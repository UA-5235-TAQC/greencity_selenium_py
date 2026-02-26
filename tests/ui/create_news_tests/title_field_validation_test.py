
from components.tag_item import TagItem
from pages.home_page import HomePage
from pages.create_edit_news.create_news_page import CreateNewsPage
from data.config import Config
from enums.news_tag import EcoNewsTag

NEWS_TITLE : str = "Title for test news"
NEWS_DESCRIPTION : str = "Description for test news Description for test news"
TAG : TagItem = TagItem(EcoNewsTag)


def login_user(driver):
    home_page = HomePage(driver).open()
    sign_in_modal = home_page.header.click_sign_in_link()
    sign_in_modal.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

def test_title_field_validation(get_driver):
    login_user(get_driver)

    create_news_page = CreateNewsPage(get_driver)
    create_news_page.open()
    assert create_news_page.get_current_url() == f"{Config.BASE_UI_GREEN_CITY_URL}/news/create-news"


