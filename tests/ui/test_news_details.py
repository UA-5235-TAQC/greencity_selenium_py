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