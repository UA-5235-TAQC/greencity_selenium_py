import allure

from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage


@allure.epic("Eco News")
@allure.feature("News Management")
@allure.story("Create and Delete News Workflow")
def test_create_and_delete_news(get_driver, logged_in_user) -> None:
    create_page = CreateNewsPage(get_driver)
    news_page = NewsPage(get_driver)
    details_page = NewsDetailsPage(get_driver)

    news_data = {
        "title": "NEWS CREATED FOR DELETION",
        "tag": EcoNewsTag.EDUCATION.en,
        "content": "This is a test news article that will be deleted after the execution."
    }

    news_page.open()
    with allure.step("Navigate to Create News and fill mandatory fields"):
        create_page.open().header.change_to_en()
        create_page.create_news(
            title=news_data["title"],
            tags=[news_data["tag"]],
            content=news_data["content"]
        )
        create_page.click_publish()

    with allure.step("Identify the ID of the newly created news from the list"):
        new_id = news_page.get_latest_news_id()
        allure.attach(str(new_id), name="Created News ID")

    with allure.step(f"Verify news content on details page (ID: {new_id})"):
        details_page.open(new_id)
        assert details_page.is_page_opened(), "News details page failed to load"
        assert details_page.get_title_value() == news_data["title"], "Title does not match input"
        assert news_data["content"] in details_page.get_content_text(), "Content mismatch"

    with allure.step("Delete the news and confirm"):
        details_page.delete_news_by_id(new_id)

    with allure.step("Verify that news is no longer accessible"):
        assert not details_page.is_news_exist(new_id), f"News with ID {new_id} should have been deleted"
