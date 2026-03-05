import allure
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.edit_news_page import EditNewsPage

NEWS_TITLE: str = "Test News Updated"
NOT_VALID_CONTENT = "Not valid content(("



@allure.feature("Edit News")
@allure.story("Content field validation")
def test_edit_content_not_shorter_than_20_chars_not_accepted(eco_news_details_page):
    driver = eco_news_details_page.driver
    existing_news_id = eco_news_details_page.get_news_id()
    with allure.step(f"Open Edit News page for news ID: {existing_news_id}"):
        edit_news_page = EditNewsPage(driver, news_id=existing_news_id)
        edit_news_page.open()
        edit_news_page.header.change_to_en()

    with allure.step("Enter invalid content (<20 chars) while editing"):
        edit_news_page.content_component.enter_content(NOT_VALID_CONTENT)

        assert edit_news_page.content_component.is_content_invalid(), "Content field should be marked as invalid"

    with allure.step("Enter valid title and select tag"):
        edit_news_page.enter_title(NEWS_TITLE)

        edit_news_page.clear_all_selected_tags()
        edit_news_page.select_tag(EcoNewsTag.NEWS.en)

    with allure.step("Verify that Edit button is disabled due to invalid content"):
        assert edit_news_page.is_edit_button_enabled() is False, "Edit button should be disabled for short content"