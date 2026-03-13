import allure
from allure_commons.types import Severity

from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.news_details_page import NewsDetailsPage


@allure.tag("Edit News")
@allure.epic("EcoNews UI")
@allure.feature("Edit News")
@allure.story("Empty title field validation")
@allure.severity(Severity.NORMAL)
@allure.issue("15")
@allure.description(
    "Verify that the Edit News page disables the Edit button and"
    " highlights the title field when the title is empty"
)
def test_empty_title_field(eco_news_details_page: NewsDetailsPage):
    """ Verify that the Edit News page disables the Edit
    button and highlights the title field when the title is empty. """
    with allure.step("Change language to English and open Edit News page"):
        eco_news_details_page.header.change_to_en()
        eco_news_details_page.click_edit_button()
        eco_news_id = eco_news_details_page.get_news_id()
        edit_news_page = EditNewsPage(eco_news_details_page.driver, eco_news_id)
        assert edit_news_page.is_page_opened(), "Edit News page should be opened"

    with allure.step("Verify behavior for empty title"):
        original_title = edit_news_page.get_title_value()
        edit_news_page.enter_title("")

        title_counter = edit_news_page.get_title_counter_text()
        assert title_counter == "0/170", "Title counter should be 0/170"
        assert edit_news_page.get_title_length() == 0, "Title length should be 0 by default"
        assert edit_news_page.get_title_value() == "", "Title should be empty by default"
        assert edit_news_page.is_title_invalid(), "Title border should be red (ng-invalid) when empty"
        assert not edit_news_page.is_edit_button_enabled(), "Edit button should be disabled when title is empty"

    with allure.step("Restore original title and verify valid state"):
        edit_news_page.enter_title(original_title)
        expected_title_length = len(original_title)
        expected_title_counter = f"{expected_title_length}/170"

        assert edit_news_page.get_title_counter_text() == expected_title_counter, \
            "Title counter should reflect the current title length"
        assert edit_news_page.get_title_length() == expected_title_length, \
            "Title length should match the length of the restored title"
        assert edit_news_page.get_title_value() == original_title, \
            "Title should be the same as the initially captured title"
        assert not edit_news_page.is_title_invalid(), "Red highlight should disappear when title is valid"
        assert edit_news_page.is_edit_button_enabled(), \
            "Edit button should become enabled after all fields are valid"
