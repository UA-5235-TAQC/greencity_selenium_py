import allure
from allure_commons.types import Severity

from data.ui_news_test_data import NewsTestData
from pages.create_edit_news.create_news_page import CreateNewsPage
import re


@allure.epic("EcoNews UI")
@allure.feature("Create News")
@allure.story("Content component validation")
@allure.issue("7")
@allure.title("Validate Main Text field for min/max length and Publish button state")
@allure.tag("Create News")
@allure.severity(Severity.NORMAL)
def test_main_text_field_validation(driver_with_login):
    """
    Verify the validation behavior of the Main Text (content) field in the Create News form.

    Steps:
    1. Login and open Create News page.
    2. Fill required fields except content.
    3. Enter too short content (<20 characters) and verify error message and disabled Publish.
    4. Enter too long content (>63,206 characters) and verify error message and disabled Publish.
    5. Enter valid content (>=20 characters) and verify error disappears and Publish button is enabled.
    6. Click Publish to submit the news.
    """
    with allure.step("Login and open create news page"):
        create_news_page = CreateNewsPage(driver_with_login)
        create_news_page.set_window_size(2560, 1440)
        create_news_page.open().header.change_to_en()
        assert "/news/create-news" in create_news_page.get_current_url()

    with allure.step("Fill required fields except content"):
        create_news_page.enter_title("Test")
        create_news_page.select_tag("News")

    with allure.step("Enter 10 characters in Main Text"):
        create_news_page.content_component.enter_content("Short text")

    with allure.step("Verify error message is displayed"):
        assert create_news_page.content_component.is_content_warning_displayed()
        warning_text = create_news_page.content_component.get_content_warning_text()

        assert re.search(r"20", warning_text)
        assert re.search(r"63[\s,]?206", warning_text)

    with allure.step("Verify Publish button is disabled"):
        assert not create_news_page.is_publish_button_enabled()

    with allure.step("Enter content longer than 63,206 characters"):
        too_long_content = "A" * 63207
        create_news_page.content_component.set_content_via_js(too_long_content)

    with allure.step("Verify error message is displayed for too long content"):
        assert create_news_page.content_component.is_content_warning_displayed()
        warning_text = create_news_page.content_component.get_content_warning_text()

        assert re.search(r"20", warning_text)
        assert re.search(r"63[\s,]?206", warning_text)

    with allure.step("Verify Publish button is disabled for too long content"):
        assert not create_news_page.is_publish_button_enabled()

    with allure.step("Enter valid content (25+ chars)"):
        create_news_page.content_component.enter_content(NewsTestData.VALID_CONTENT)

    with allure.step("Verify error disappears"):
        assert create_news_page.content_component.is_content_valid()

    with allure.step("Verify Publish button becomes enabled"):
        assert create_news_page.is_publish_button_enabled()

    with allure.step("Click Publish"):
        create_news_page.click_publish_ubs()
