import allure
from allure_commons.types import Severity
from pages.news_details_page import NewsDetailsPage


@allure.tag("Edit News")
@allure.epic("EcoNews UI")
@allure.feature("Edit News")
@allure.story("Verify that only the author can see the 'Edit news' button")
@allure.severity(Severity.CRITICAL)
class TestEditButtonVisibility:
    """ Verify that the 'Edit news' button is visible and enabled only to the author of the news. """

    @allure.issue("11")
    @allure.title("Verify that the 'Edit news' button is visible only to the author of the news")
    def test_edit_button_visible_to_author(self, eco_news_details_page: NewsDetailsPage):
        """ Verify that the 'Edit news' button is visible and enabled only to the author of the news. """
        eco_news_details_page.header.change_to_en()
        assert eco_news_details_page.is_edit_button_visible(), "Edit news button should be visible to the author"
        assert eco_news_details_page.is_edit_button_enabled(), "Edit news button should be enabled for the author"
        assert eco_news_details_page.get_edit_button_text() == "Edit news", "Edit button text is incorrect"

    @allure.issue("12")
    @allure.title("Verify that the 'Edit news' button is not visible for news created by other users")
    def test_edit_button_not_visible_to_other_users(self, get_driver, news_created_by_second_user):
        """ Verify that the 'Edit news' button is NOT visible for news created by another user. """
        news_details_page = NewsDetailsPage(get_driver).open(news_created_by_second_user)
        assert news_details_page.is_page_opened(), "News Details page should be opened"
        assert not news_details_page.is_edit_button_visible(), "Edit news button should NOT be visible to other users"
