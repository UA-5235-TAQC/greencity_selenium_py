import allure
from allure_commons.types import Severity

from data.ui_news_test_data import TAGS_TO_SELECT, SOURCE_LINK, SOURCE_FIELD_ERROR_MESSAGE, \
    TEST_CONTENT_UA, TEST_TITLE_UA
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_page import NewsPage


@allure.epic("EcoNews UI")
@allure.feature("Create EcoNews")
@allure.story("Source Field Validation")
@allure.title("Verify Source field validation during news creation")
@allure.tag("Create News")
@allure.severity(Severity.NORMAL)
def test_source_field_validation(driver_with_login):
    """
    Verify the behavior of the Source field in the Create EcoNews page.

    Scenarios:
    1. Create a news item with mandatory fields only and publish successfully.
    2. Attempt to create a news item with an invalid source link.
       Verify that the validation error is displayed and the Publish button is disabled.
    """
    create_news: CreateNewsPage = NewsPage(driver_with_login).open().click_create_news()
    create_news.header.change_to_uk()

    with allure.step("Create news with mandatory fields"):
        create_news.create_news(title=TEST_TITLE_UA,
                                content=TEST_CONTENT_UA,
                                tags=TAGS_TO_SELECT)

    with allure.step("Verify filled data is correct"):
        assert create_news.get_title_value() == TEST_TITLE_UA, "Title field value did not match"
        assert sorted(create_news.get_selected_tags()) == sorted(TAGS_TO_SELECT), "Selected tags did not match"
        assert create_news.content_component.get_content_text() == TEST_CONTENT_UA, "Content text did not match"
        assert create_news.is_publish_button_enabled(), "Publish button should be enabled"

    with allure.step("Publish news"):
        create_news.click_publish()

    with allure.step("Verify Eco News page opened"):
        eco_news_page = NewsPage(create_news.driver)
        assert eco_news_page.is_page_opened(), "Eco News page should be opened after publishing"

    with allure.step("Return to Create News page"):
        eco_news_page.click_create_news()

    with allure.step("Create news with invalid source link"):
        create_news.create_news(title=TEST_TITLE_UA,
                                source=SOURCE_LINK,
                                content=TEST_CONTENT_UA,
                                tags=TAGS_TO_SELECT)

    with allure.step("Verify validation source field error and disabled publish button"):
        assert create_news.get_title_value() == TEST_TITLE_UA, "Title field value did not match"
        assert sorted(create_news.get_selected_tags()) == sorted(TAGS_TO_SELECT), "Selected tags did not match"
        assert create_news.content_component.get_content_text() == TEST_CONTENT_UA, "Content text did not match"
        assert SOURCE_FIELD_ERROR_MESSAGE in create_news.get_source_message_text()
        assert not create_news.is_publish_button_enabled(), "Publish button should be disabled"
