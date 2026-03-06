import pytest
import allure

from enums.language import Language
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_page import NewsPage
from components.news_list_item_component import NewsListItemComponent
from data.ui_news_test_data import NewsTestData
import pytest_check as check
from allure_commons.types import Severity


@allure.tag("Create News")
@allure.epic("EcoNews Management")
@allure.feature("Create News")
@allure.story("Verify news tag selection behavior")
@allure.severity(Severity.NORMAL)
@allure.issue("5")
class TestTagSelection:
    """ Verify news tag selection behavior. """

    @allure.description("Verify max 3 tags selectable behavior")
    def test_four_tags_selection_blocked(self, eco_page: NewsPage):
        """ Test that selecting a fourth tag is blocked (max 3 tags selectable). """
        four_tags = [
            EcoNewsTag.NEWS,
            EcoNewsTag.EVENTS,
            EcoNewsTag.EDUCATION,
            EcoNewsTag.INITIATIVES
        ]

        tags_en = EcoNewsTag.get_en(four_tags)

        create_news_page: CreateNewsPage = eco_page.click_create_news()
        assert create_news_page.is_page_opened(), "Create News page should be opened"

        create_news_page.enter_title(NewsTestData.TEST_TITLE_EN)
        create_news_page.enter_source(NewsTestData.TEST_SOURCE_EN)
        create_news_page.content_component.enter_content(NewsTestData.VALID_CONTENT)
        create_news_page.image_component.upload_image(
            str(NewsTestData.TEST_FILE)
        ).submit_crop()

        create_news_page.select_tags(tags_en)

        selected_tags = create_news_page.get_selected_tags()
        check.equal(len(selected_tags), 3, "Only 3 tags should be selectable")
        check.is_false("Initiatives" in selected_tags, "Fourth tag should not be selected")

        create_news_page.click_cancel()
        cancel_modal = create_news_page.cancel_modal
        assert cancel_modal.is_visible(), "Confirmation modal should appear after clicking Cancel"

        cancel_modal.click_yes_cancel()

    @allure.description("Verify Create News publishing with multiple tags in different locales")
    @pytest.mark.parametrize("language", [Language.EN, Language.UK])
    def test_tag_selection(self, eco_page: NewsPage, language: str):
        """
        Test publishing news with predefined NewsTestData for one or multiple tags.
        Language param selects English ('en') or Ukrainian ('ua') data.
        """
        create_news_page: CreateNewsPage = eco_page.click_create_news()
        assert create_news_page.is_page_opened(), "Create News page should be opened"

        if language == Language.EN:
            create_news_page.header.change_to_en()
            NewsTestData.apply_to_en(create_news_page)
            expected_tags = EcoNewsTag.get_en_upper(NewsTestData.TEST_TAGS)
            expected_title = NewsTestData.TEST_TITLE_EN
        else:
            create_news_page.header.change_to_uk()
            NewsTestData.apply_to_ua(create_news_page)
            expected_tags = EcoNewsTag.get_ua_upper(NewsTestData.TEST_TAGS)
            expected_title = NewsTestData.TEST_TITLE_UA

        create_news_page.click_publish()

        assert eco_page.is_page_opened(), "Eco News page should be opened after publishing"

        news_card: NewsListItemComponent = eco_page.get_latest_created_news()
        check.equal(news_card.get_title(), expected_title, f"News should have title '{expected_title}'")
        check.is_true(news_card.has_tags(expected_tags), f"News should have tags {expected_tags}")

    @allure.description("Verify creating news with single tag")
    def test_single_tag_selection(self, eco_page: NewsPage):
        """ Test creating news with a single tag. """
        create_news_page: CreateNewsPage = eco_page.click_create_news()
        create_news_page.enter_title(NewsTestData.TEST_TITLE_EN)
        create_news_page.enter_source(NewsTestData.TEST_SOURCE_EN)
        create_news_page.content_component.enter_content(NewsTestData.VALID_CONTENT)
        tag = EcoNewsTag.get_en_upper([EcoNewsTag.NEWS])
        create_news_page.select_tags(tag)
        create_news_page.click_publish()

        news_card = eco_page.get_latest_created_news()

        check.equal(news_card.get_title(), NewsTestData.TEST_TITLE_EN)
        check.equal(news_card.get_tags(), tag)

    @allure.description("Verify creating news with three tags")
    def test_three_tags_selection(self, eco_page: NewsPage):
        """ Test creating news with exactly three tags. """
        create_news_page: CreateNewsPage = eco_page.click_create_news()
        create_news_page.enter_title(NewsTestData.TEST_TITLE_EN)
        create_news_page.enter_source(NewsTestData.TEST_SOURCE_EN)
        create_news_page.content_component.enter_content(NewsTestData.VALID_CONTENT)

        tags_to_select = [
            EcoNewsTag.NEWS,
            EcoNewsTag.EVENTS,
            EcoNewsTag.EDUCATION
        ]
        selected_tags = EcoNewsTag.get_en_upper(tags_to_select)
        create_news_page.select_tags(selected_tags)
        create_news_page.click_publish()

        news_card = eco_page.get_latest_created_news()

        check.equal(news_card.get_title(), NewsTestData.TEST_TITLE_EN)
        check.equal(news_card.get_tags(), selected_tags)
