import allure
from selenium.webdriver.support.ui import WebDriverWait

MODIFIED_TEXT = "Modified text for cancel test"

@allure.feature("Edit News")
@allure.issue("18")
@allure.story("Cancel editing behavior")
def test_cancel_editing_discards_changes(eco_news_details_page):

    with allure.step("Open Edit News page"):
        edit_page = eco_news_details_page.click_edit_button()
        edit_page.open()
        edit_page.header.change_to_en()

        original_content = edit_page.content_component.get_content_text()

    with allure.step("Modify content"):
        edit_page.content_component.enter_content(MODIFIED_TEXT)

    with allure.step("Click Cancel"):
        edit_page.click_cancel()

    with allure.step("Verify cancel modal appears"):
        cancel_modal = edit_page.cancel_modal

        cancel_modal.wait_until_visible()
        assert cancel_modal.is_visible()

    with allure.step("Confirm Yes, cancel"):
        edit_page.cancel_modal.click_yes_cancel()

    with allure.step("Verify redirection from Edit page"):
        WebDriverWait(edit_page.driver, 5).until(
            lambda d: "create-news" not in d.current_url
        )


    with allure.step("Reopen same news and verify content unchanged"):
        edit_page.open()
        current_content = edit_page.content_component.get_content_text()

        assert current_content == original_content