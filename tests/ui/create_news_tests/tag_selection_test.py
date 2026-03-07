import allure
from allure_commons.types import Severity
import pytest
import uuid
from enums.language import Language
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_page import NewsPage
from components.news_list_item_component import NewsListItemComponent
from data.ui_news_test_data import NewsTestData
import pytest_check as check


@allure.epic("EcoNews UI")
@allure.feature("Create News")
@allure.story("Tag Selection")
@allure.tag("Create News")
class TestTagSelection:
    """
    Test suite for verifying tag selection functionality in Create News page.

    Includes tests for:
    - Selecting a single tag
    - Selecting three tags
    - Attempting to select a fourth tag (blocked)
    """

    @allure.title("Check selection of one tag")
    @allure.severity(Severity.NORMAL)
    def test_check_one_tag_selection(self, tag_selection_environment):
        """Test checks selection of one tag."""
        create_news_page, news_page = tag_selection_environment
        assert create_news_page.is_page_opened(), "Create News page should be opened"

        tag_names = EcoNewsTag.get_en_upper([EcoNewsTag.NEWS])
        create_news_page.create_news(
            title="Test Tag Selection",
            tags=tag_names,
            content="Test content with more than 20 characters."
        )
        create_news_page.click_publish()

        assert news_page.is_page_opened(), "Should return to News page"
        news_item = news_page.get_news_card_by_index(0)
        assert news_item.get_title() == "Test Tag Selection", "Title mismatch"
        assert news_item.has_tags(tag_names), f"Tags mismatch. Expected: {tag_names}, Actual: {news_item.get_tags()}"

    @allure.title("Check selection of three tags")
    @allure.severity(Severity.NORMAL)
    def test_check_three_tags_selection(self, tag_selection_environment):
        """Test checks selection of three tags."""
        create_news_page, news_page = tag_selection_environment
        assert create_news_page.is_page_opened(), "Create News page should be opened"

        tag_names = EcoNewsTag.get_en_upper([EcoNewsTag.NEWS, EcoNewsTag.EVENTS, EcoNewsTag.EDUCATION])

        create_news_page.create_news(
            title="Test Three Tags",
            tags=tag_names,
            content="Test content with more than 20 characters."
        )
        create_news_page.click_publish()

        assert news_page.is_page_opened(), "Should return to News page"
        news_item = news_page.get_news_card_by_index(0)
        assert news_item.get_title() == "Test Three Tags", "Title mismatch"
        assert news_item.has_tags(tag_names), f"Tags mismatch. Expected: {tag_names}, Actual: {news_item.get_tags()}"

    @allure.title("Verify that selecting a 4th tag is blocked")
    @allure.severity(Severity.CRITICAL)
    def test_check_four_tags_selection(self, tag_selection_environment):
        """Test verifies that selecting a 4th tag is blocked."""
        create_news_page, news_page = tag_selection_environment
        assert create_news_page.is_page_opened(), "Create News page should be opened"

        tags = [EcoNewsTag.NEWS, EcoNewsTag.EVENTS, EcoNewsTag.EDUCATION, EcoNewsTag.INITIATIVES]
        tag_names = [tag.en for tag in tags]

        create_news_page.enter_title("Test 4 Tags Block").select_tags(tag_names)

        assert not create_news_page.publish_btn.is_enabled(), \
            "Publish button should be disabled when 4 tags are selected"

        create_news_page.cancel_btn.click()
        create_news_page.cancel_modal.click_yes_cancel()
        assert news_page.is_page_opened(), "Should return to News page after cancellation"

    @allure.issue("5")
    @allure.title("Verify max 3 tags selectable behavior")
    @allure.severity(Severity.CRITICAL)
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

    @allure.issue("5")
    @allure.title("Verify Create News publishing with multiple tags in different locales")
    @allure.severity(Severity.NORMAL)
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

    @allure.issue("5")
    @allure.title("Verify creating news with single tag")
    @allure.severity(Severity.NORMAL)
    def test_single_tag_selection(self, eco_page: NewsPage):
        """ Test creating news with a single tag. """
        create_news_page: CreateNewsPage = eco_page.click_create_news()
        title = f"{NewsTestData.TEST_TITLE_EN} {uuid.uuid4().hex[:6]}"
        create_news_page.enter_title(title)
        create_news_page.enter_source(NewsTestData.TEST_SOURCE_EN)
        create_news_page.content_component.enter_content(NewsTestData.VALID_CONTENT)
        tag = EcoNewsTag.get_en_upper([EcoNewsTag.NEWS])
        create_news_page.select_tags(tag)
        create_news_page.click_publish()

        news_card = eco_page.get_news_card_by_title(title)

        check.equal(news_card.get_title(), title)
        check.equal(news_card.get_tags(), tag)

    @allure.issue("5")
    @allure.title("Verify creating news with three tags")
    @allure.severity(Severity.NORMAL)
    def test_three_tags_selection(self, eco_page: NewsPage):
        """ Test creating news with exactly three tags. """
        create_news_page: CreateNewsPage = eco_page.click_create_news()
        title = f"{NewsTestData.TEST_TITLE_EN} {uuid.uuid4().hex[:6]}"
        create_news_page.enter_title(title)
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

        news_card = eco_page.get_news_card_by_title(title)

        check.equal(news_card.get_title(), title)
        check.equal(news_card.get_tags(), selected_tags)
