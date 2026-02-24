import allure
import pytest
from pages.news_details_page import NewsDetailsPage

@allure.feature("News Details")
class TestNewsDetails:
    news_id = 3174

    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify news details elements and content")
    def test_verify_news_content(self, get_driver):
        news_page = NewsDetailsPage(get_driver, self.news_id)
        news_page.open()

        assert news_page.get_title_value() != "", "Title should not be empty"
        assert news_page.get_post_date() != "", "Post date should not be empty"
        assert news_page.get_author() != "", "Author should not be empty"
        assert news_page.get_id() == self.news_id, "ID mismatch"
        
        assert "http" in news_page.get_news_image_src(), "Image src should be a valid URL"
        tags = news_page.get_tags()
        assert isinstance(tags, list), "Tags should be a list"
        
    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify like functionality")
    def test_like_functionality(self, get_driver):
        news_page = NewsDetailsPage(get_driver, self.news_id)
        news_page.open()

        initial_likes = news_page.get_likes_count()
        is_liked = news_page.is_like_active()

        news_page.click_like_button()
        
        expected_likes = initial_likes - 1 if is_liked else initial_likes + 1
        news_page.wait_for_likes_to_change(expected_likes)

        assert news_page.get_likes_count() == expected_likes
        assert news_page.is_like_active() != is_liked, "Like status should toggle"

    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify navigation and UI state")
    def test_ui_elements_state(self, get_driver):
        news_page = NewsDetailsPage(get_driver, self.news_id)
        news_page.open()

        state = news_page.is_edit_button_enabled()
        assert isinstance(state, bool)

        news_page.click_back_to_news_button()
        assert "news" in get_driver.current_url

    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify 'Recommended News' section title")
    @allure.severity(allure.severity_level.NORMAL)
    def test_recommended_section_title(self, get_driver):
        page = NewsDetailsPage(get_driver, self.news_id)
        page.open()
        
        expected_title = "May be interesting for you" 
        actual_title = page.recommended_news.get_title_text()
        
        assert actual_title == expected_title, \
            f"Expected title '{expected_title}', but got '{actual_title}'"

    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify that 3 recommended news cards are displayed")
    @allure.description("Checks that the count of recommended cards equals 3")
    def test_recommended_cards_count(self, get_driver):
        page = NewsDetailsPage(get_driver, self.news_id)
        page.open()
        
        cards = page.recommended_news.get_all_cards()
        
        assert len(cards) == 3, f"Expected 3 cards, but found {len(cards)}"

    @pytest.mark.skip(reason="Test just for object's methods testing")
    @allure.title("Verify navigation to a recommended news card")
    def test_click_recommended_card(self, get_driver):
        page = NewsDetailsPage(get_driver, self.news_id)
        page.open()
        
        first_card = page.recommended_news.get_card_by_index(0)
        
        first_card.click()
        
        assert f"/news/" in get_driver.current_url
        assert str(self.news_id) not in get_driver.current_url