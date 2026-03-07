import allure
from allure_commons.types import Severity
from data.config import Config
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage


@allure.epic("EcoNews UI")
@allure.feature("Delete News")
@allure.story("Create and Delete News Workflow")
@allure.title("Verify that an author can create a news article and delete it successfully")
@allure.tag("Delete News")
@allure.severity(Severity.NORMAL)
def test_create_and_delete_news(driver_with_login) -> None:
    """
    Verify that an author can create a news article, view it in the news list,
    and delete it, ensuring it is no longer accessible afterwards.
    """
    create_page = CreateNewsPage(driver_with_login)
    news_page = NewsPage(driver_with_login)
    details_page = NewsDetailsPage(driver_with_login)

    news_data = {
        "title": "TEST NEWS FOR DELETION",
        "tag": EcoNewsTag.EDUCATION.en,
        "content": "This is a test news article that will be deleted after the execution."
    }

    with allure.step("1. Navigate to Create News and publish a new article"):
        news_page.open()
        create_page.open()
        create_page.header.change_to_en()
        create_page.create_news(
            title=news_data["title"],
            tags=[news_data["tag"]],
            content=news_data["content"]
        )
        create_page.click_publish()

    with allure.step("2. Identify and open the newly created news from the list"):
        news_page.open()

        news_page.wait_for(
            lambda _: news_page.get_latest_created_news().get_title() == news_data["title"],
            timeout=Config.EXPLICITLY_WAIT
        )

        latest_card = news_page.get_latest_created_news()
        latest_card.open_news_by_card()

    with allure.step("3. Verify news content and extract its ID"):
        details_page.wait_until_opened()
        news_id = details_page.get_news_id()
        allure.attach(str(news_id), name="Extracted News ID")

        assert details_page.get_title_value() == news_data["title"]
        assert news_data["content"] in details_page.get_content_text()

    with allure.step(f"4. Delete the news (ID: {news_id})"):
        details_page.delete_news_by_id(news_id)

    with allure.step("5. Verify that news is no longer accessible"):
        news_page.open()
        news_page.reload()
        if len(news_page.news_card_items) > 0:
            latest_news = news_page.get_latest_created_news()
            assert latest_news.get_title() != news_data[
                "title"], f"News with title '{news_data['title']}' still exists as the latest news card!"
            for card in news_page.news_card_items:
                assert card.get_title() != news_data[
                    "title"], f"News with title '{news_data['title']}' still exists in the news list!"
