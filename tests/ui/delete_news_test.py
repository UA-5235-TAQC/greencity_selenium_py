from pages.news_details_page import NewsDetailsPage

news_id = 3841


def test_delete_news_by_id(get_driver, logged_in_user) -> None:
    news_details = NewsDetailsPage(get_driver)
    news_details.header.change_to_en()
    news_details.delete_news_by_id(news_id)
    news_details.open(news_id)
    assert news_details.is_page_opened() is False
