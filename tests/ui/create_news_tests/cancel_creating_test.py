import allure
from allure_commons.types import Severity
from data.ui_news_test_data import NewsTestData
from pages.create_edit_news.create_news_page import CreateNewsPage


@allure.epic("EcoNews UI")
@allure.feature("Create EcoNews")
@allure.story("Cancel news creation")
@allure.title("Verify cancel button behavior and redirection after confirmation")
@allure.tag("Create News")
@allure.severity(Severity.NORMAL)
def test_cancel_button_behavior(driver_with_login):
    """
    Verify that the user can cancel the EcoNews creation process.

    Steps:
    1. Open the Create News page and switch language to English.
    2. Fill in the news title and content.
    3. Click the Cancel button.
    4. Verify that the cancellation confirmation modal appears.
    5. Verify the modal text content.
    6. Confirm cancellation.
    7. Verify that the user is redirected away from the Create News page.
    """

    with allure.step("Open Create News page and switch language to English"):
        create_news_page = CreateNewsPage(driver_with_login)
        create_news_page.open().header.change_to_en()
        assert create_news_page.is_page_opened(), "Create News page was not opened"

    with allure.step("Fill the news creation form"):
        create_news_page.enter_title(NewsTestData.TEST_TITLE_EN)
        create_news_page.content_component.enter_content(NewsTestData.TEST_CONTENT_EN)

    with allure.step("Click Cancel button"):
        create_news_page.cancel_btn.click()

    with allure.step("Verify confirmation modal is displayed"):
        cancel_modal = create_news_page.cancel_modal
        assert cancel_modal.is_visible(), "Confirmation modal should be visible"

    with allure.step("Verify modal warning text"):
        assert cancel_modal.get_warning_title_text() == "All created content will be lost."
        assert cancel_modal.get_warning_subtitle_text() == "Do you still want to cancel news creating?"

    with allure.step("Confirm cancellation"):
        ubs_courier_page = cancel_modal.click_yes_cancel()

    with allure.step("Wait until user is redirected from Create News page"):
        ubs_courier_page.wait_for(lambda d: "/news/create-news" not in d.current_url)

    with allure.step("Verify redirection to UBS Courier page"):
        assert ubs_courier_page.is_page_opened(), \
            "Should be redirected to UBS Courier page after cancellation"

    with allure.step("Verify that Create News URL is no longer present"):
        assert "/news/create-news" not in driver_with_login.current_url, \
            "User is still on the Create News URL"
