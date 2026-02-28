import allure

from enums.news_tag import EcoNewsTag
from pages.news_page import NewsPage


NEWS_TITLE = "Hello World"
SOURCE_LINK = "hello"
SOURCE_FIELD_ERROR_MESSAGE = "Please add the link of original article"
CONTENT = "Olaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
TAGS = [EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en]


@allure.epic("UI Tests")
@allure.feature("News Creation")
@allure.story("Source Field Validation")
def test_source_field_validation(create_news):

    with allure.step("Create news with mandatory fields"):
        create_news.create_news(title=NEWS_TITLE,
                                content=CONTENT,
                                tags=TAGS)

    with allure.step("Verify filled data is correct"):
        assert create_news.get_title_value() == NEWS_TITLE, "Title field value did not match"
        assert create_news.get_selected_tags() == TAGS, "Selected tags did not match"
        assert create_news.content_component.get_content_text() == CONTENT, "Content text did not match"
        assert create_news.is_publish_button_enabled(), "Publish button should be enabled"

    with allure.step("Publish news"):
        create_news.click_publish()

    with allure.step("Verify Eco News page opened"):
        eco_news_page = NewsPage(create_news.driver)
        assert eco_news_page.is_page_opened(), "Eco News page should be opened after publishing"

    with allure.step("Return to Create News page"):
        eco_news_page.click_create_news()

    with allure.step("Create news with invalid source link"):
        create_news.create_news(title=NEWS_TITLE,
                                source=SOURCE_LINK,
                                content=CONTENT,
                                tags=TAGS)

    with allure.step("Verify validation source field error and disabled publish button"):
        assert create_news.get_title_value() == NEWS_TITLE, "Title field value did not match"
        assert create_news.get_selected_tags() == TAGS, "Selected tags did not match"
        assert create_news.content_component.get_content_text() == CONTENT, "Content text did not match"
        assert SOURCE_FIELD_ERROR_MESSAGE in create_news.get_source_message_text()
        assert not create_news.is_publish_button_enabled(), "Publish button should be disabled"






