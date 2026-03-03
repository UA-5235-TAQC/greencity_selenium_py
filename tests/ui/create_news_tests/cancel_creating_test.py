import allure
from pages.create_edit_news.create_news_page import CreateNewsPage

TEST_TITLE_EN = "Test"
TEST_CONTENT_EN = "Test content with 20 chars."


@allure.feature("Create News")
@allure.story("Cancel news creation")
@allure.severity(allure.severity_level.NORMAL)
@allure.description(
    "Verify that clicking the Cancel button triggers a confirmation modal, "
    "and selecting 'Yes, cancel' closes the form and redirects away"
)
def test_cancel_button_behavior(driver_with_login):

    # Open the page and change language
    create_news_page = CreateNewsPage(driver_with_login)
    create_news_page.open().header.change_to_en()
    assert create_news_page.is_page_opened(), "Create News page was not opened"

    # Fill the form
    create_news_page.enter_title(TEST_TITLE_EN)
    create_news_page.content_component.enter_content(TEST_CONTENT_EN)

    create_news_page.cancel_btn.click()

    # Interaction with the modal
    cancel_modal = create_news_page.cancel_modal
    assert cancel_modal.is_visible(), "Confirmation modal should be visible"

    assert cancel_modal.get_warning_title_text() == "All created content will be lost."
    assert cancel_modal.get_warning_subtitle_text() == "Do you still want to cancel news creating?"

    # Confirm cancellation and verify redirect
    ubs_courier_page = cancel_modal.click_yes_cancel()

    # wait the current URL no longer 'create-news'
    ubs_courier_page.wait_for(lambda d: "/news/create-news" not in d.current_url)

    assert ubs_courier_page.is_page_opened(), \
        "Should be redirected to UBS Courier page after cancellation"

    # Check that URL has changed
    assert "/news/create-news" not in driver_with_login.current_url, \
        "User is still on the Create News URL"