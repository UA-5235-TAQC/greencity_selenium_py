import allure
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage

NEWS_TITLE: str = "Test News"
NOT_VALID_CONTENT = "Not valid content(("

@allure.feature("Create News")
@allure.story("Content field validation")
def test_content_not_shorter_than_20_chars_not_accepted(logged_in_user):
    driver = logged_in_user

    with allure.step("Open Create News page"):
        create_news_page = CreateNewsPage(driver)
        create_news_page.open()
        create_news_page.header.change_to_en()

    with allure.step("Enter invalid content (<20 chars)"):
        create_news_page.enter_content(NOT_VALID_CONTENT)
        assert create_news_page.is_content_field_invalid()

    with allure.step("Enter valid title and select tag"):
        create_news_page.enter_title(NEWS_TITLE)
        create_news_page.select_tag(EcoNewsTag.NEWS.en)
        assert create_news_page.is_publish_button_enabled() is False