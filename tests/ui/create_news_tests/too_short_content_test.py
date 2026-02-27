import allure
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.edit_news_page import EditNewsPage

NEWS_TITLE: str = "Test News Updated"
NOT_VALID_CONTENT = "Not valid content(("
EXISTING_NEWS_ID = 3588


@allure.feature("Edit News")
@allure.story("Content field validation")
def test_edit_content_not_shorter_than_20_chars_not_accepted(logged_in_user):
    driver = logged_in_user

    with allure.step(f"Open Edit News page for news ID: {EXISTING_NEWS_ID}"):
        edit_news_page = EditNewsPage(driver, news_id=EXISTING_NEWS_ID)
        edit_news_page.open()
        edit_news_page.header.change_to_en()

    with allure.step("Enter invalid content (<20 chars) while editing"):
        edit_news_page.enter_content(NOT_VALID_CONTENT)

        assert edit_news_page.is_content_field_invalid(), "Content field should be marked as invalid"

    with allure.step("Enter valid title and select tag"):
        edit_news_page.enter_title(NEWS_TITLE)

        edit_news_page.clear_all_selected_tags()
        edit_news_page.select_tag(EcoNewsTag.NEWS.en)

    with allure.step("Verify that Edit button is disabled due to invalid content"):
        assert edit_news_page.is_edit_button_enabled() is False, "Edit button should be disabled for short content"