import allure
from allure_commons.types import Severity
import pytest_check as check
from components.news_list_item_component import NewsListItemComponent
from data.config import Config
from data.ui_news_test_data import TEST2_FILE, TEST_SOURCE_EN
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage


@allure.tag("Edit News")
@allure.epic("EcoNews UI")
@allure.feature("Edit News")
@allure.story("Verify author can edit their own news and changes are saved")
@allure.severity(Severity.CRITICAL)
@allure.issue("13")
@allure.description("Verify that the author can edit their own news and the changes are saved")
def test_verify_author_can_edit_own_news(eco_news_details_page: NewsDetailsPage):
    """ Verify that the author can edit their own news and the changes are saved. """
    eco_news_details_page.header.change_to_en()

    with allure.step("Store original news data"):
        original_title = eco_news_details_page.get_title_value()
        original_tags = eco_news_details_page.get_tags()
        original_content = eco_news_details_page.get_content_text()
        original_created_date = eco_news_details_page.get_post_date()
        author = eco_news_details_page.get_author()
        src = eco_news_details_page.get_news_image_src()

    with allure.step("Verify news details page initial state"):
        assert eco_news_details_page.are_tags_visible(), "Tags should be visible"
        assert eco_news_details_page.is_post_date_visible(), "Post date should be visible"
        assert eco_news_details_page.is_author_visible(), "Author name should be visible"
        assert author == eco_news_details_page.header.get_user(), "Author should be pre-filled"
        assert eco_news_details_page.is_content_visible(), "Content should be visible"
        assert eco_news_details_page.is_news_image_visible(), "News image should be visible"
        assert eco_news_details_page.is_news_image_present(), "News image should be present"
        assert src != "", "News image source should not be empty"

    with allure.step("Open Edit News page"):
        edit_news_page: EditNewsPage = eco_news_details_page.click_edit_button().open()
        assert edit_news_page.is_page_opened(), "Edit News page should be opened"

    with allure.step("Update news fields"):
        updated_title = original_title + " Updated"
        updated_content = "Updated content for verification of edit functionality."
        updated_tags = EcoNewsTag.get_en([EcoNewsTag.EVENTS, EcoNewsTag.EDUCATION])
        edit_news_page.edit_news(
            title=updated_title,
            tags=updated_tags,
            source=TEST_SOURCE_EN,
            content=updated_content,
            image_path=str(TEST2_FILE)
        )
        assert edit_news_page.is_edit_button_enabled(), "Edit button should be enabled after valid changes"
        edit_news_page.click_edit()

    with allure.step("Verify news page after editing"):
        news_page = NewsPage(edit_news_page.driver)
        assert news_page.is_page_opened(), "User should be directed to EcoNews page"
        news_page.header.change_to_en()

    with allure.step("Open News Details page for the updated news"):
        news_card: NewsListItemComponent = news_page.get_news_card_by_index(0)
        news_details_page: NewsDetailsPage = news_card.click_image()
        assert news_details_page.is_page_opened(), "News details page should be opened"

    with allure.step("Verify updated news content"):
        news_details_page.header.change_to_en()
        assert news_details_page.is_page_opened(), "News Details page should be opened"

        actual_tags = news_details_page.get_tags()
        actual_content = news_details_page.get_content_text()
        actual_title = news_details_page.get_title_value()
        actual_src = news_details_page.get_news_image_src()
        test_author = Config.USER_NAME

        check.equal(actual_tags, updated_tags, "Tags should match updated tags")
        check.not_equal(actual_tags, original_tags, "Tags should not match original tags")
        check.equal(actual_title, updated_title, "Title should match updated title")
        check.not_equal(actual_title, original_title, "Title should not match original title")
        check.equal(news_details_page.get_author(), author, "Author should remain the same")
        check.equal(news_details_page.get_author(), news_details_page.header.get_user(), "Author should be pre-filled")
        check.equal(news_details_page.get_author(), test_author, "Author should be the test author")
        check.equal(news_details_page.get_post_date(), original_created_date, "Created date should remain the same")
        check.equal(actual_content, updated_content, "Content should match updated content")
        check.not_equal(actual_content, original_content, "Content should not match original content")
        check.is_true(news_details_page.is_news_image_visible(), "News image should be visible")
        check.is_true(news_details_page.is_news_image_present(), "News image should be present")
        check.is_true(actual_src != "", "News image source should not be empty")
        check.not_equal(actual_src, src, "News image should be updated")
