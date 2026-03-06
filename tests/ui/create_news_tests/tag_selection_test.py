import allure
from enums.news_tag import EcoNewsTag


@allure.epic("UI Tests")
@allure.feature("Eco News")
@allure.story("Tag Selection")
class TestTagSelection:

    @allure.title("Check selection of one tag")
    @allure.severity(allure.severity_level.NORMAL)
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
    @allure.severity(allure.severity_level.NORMAL)
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
    @allure.severity(allure.severity_level.CRITICAL)
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
