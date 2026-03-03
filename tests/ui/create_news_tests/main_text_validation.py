import allure

from pages.create_edit_news.create_news_page import CreateNewsPage
import re

MIN_ERROR_TEXT = "Must be a minimum of 20 and a maximum of 63,206 symbols."
VALID_CONTENT = "This is a valid test content"


@allure.feature("Create News")
@allure.issue("7")
@allure.story("Main Text field validation")
def test_main_text_field_validation(driver_with_login):

    with allure.step("Login and open create news page"):
        create_news_page = CreateNewsPage(driver_with_login)
        create_news_page.open().header.change_to_en()
        assert "/news/create-news" in create_news_page.get_current_url()

    with allure.step("Fill required fields except content"):
        create_news_page.enter_title("Test")
        create_news_page.select_tag("News")

    # ---------- Too short content ----------

    with allure.step("Enter 10 characters in Main Text"):
        create_news_page.content_component.enter_content("Short text")

    with allure.step("Verify error message is displayed"):
        assert create_news_page.content_component.is_content_warning_displayed()
        warning_text = create_news_page.content_component.get_content_warning_text()

        assert re.search(r"20", warning_text)
        assert re.search(r"63[\s,]?206", warning_text)

    with allure.step("Verify Publish button is disabled"):
        assert not create_news_page.is_publish_button_enabled()

    # ---------- Too long content ----------

    with allure.step("Enter content longer than 63,206 characters"):
        too_long_content = "A" * 63207
        create_news_page.content_component.enter_content(too_long_content)

    with allure.step("Verify error message is displayed for too long content"):
        assert create_news_page.content_component.is_content_warning_displayed()
        warning_text = create_news_page.content_component.get_content_warning_text()

        assert re.search(r"20", warning_text)
        assert re.search(r"63[\s,]?206", warning_text)

    with allure.step("Verify Publish button is disabled for too long content"):
        assert not create_news_page.is_publish_button_enabled()

    # ---------- Valid content ----------

    with allure.step("Enter valid content (25+ chars)"):
        create_news_page.content_component.enter_content(VALID_CONTENT)

    with allure.step("Verify error disappears"):
        assert create_news_page.content_component.is_content_valid()

    with allure.step("Verify Publish button becomes enabled"):
        assert create_news_page.is_publish_button_enabled()

    # ---------- Publish ----------

    with allure.step("Click Publish"):
        create_news_page.click_publish()