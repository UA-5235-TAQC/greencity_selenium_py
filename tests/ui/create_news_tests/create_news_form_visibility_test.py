import allure
import pytest
from allure_commons.types import Severity
from data.config import Config
from enums.language import Language
from pages.create_edit_news.create_news_page import CreateNewsPage
from pages.create_edit_news.news_preview_page import NewsPreviewPage
from pages.news_page import NewsPage
from data.language_data import CREATE_NEWS_LANGUAGE_DATA
from data.ui_news_test_data import NewsTestData
import pytest_check as check


@allure.tag("Create News")
@allure.epic("EcoNews Management")
@allure.feature("Create News")
@allure.story("Verify visibility and behavior of Create News form")
@allure.severity(Severity.NORMAL)
@allure.issue("3")
@allure.description("Verify that the Create News form contains the particular fields.")
@pytest.mark.parametrize("language", [Language.EN, Language.UK])
def test_verify_create_news_form_fields_visibility(create_news_page: CreateNewsPage, language: Language):
    """ Verify that the Create News form contains the particular fields. """
    create_news_page.header.change_to_en() if language == Language.EN else create_news_page.header.change_to_uk()
    # 1. Title
    title_counter = create_news_page.get_title_counter_text()
    assert title_counter == "0/170", \
        f"Title counter should be '0/170', but was '{title_counter}'"

    title_length = create_news_page.get_title_length()
    assert title_length == 0, \
        f"Title length should be 0 by default, but was {title_length}"

    title_value = create_news_page.get_title_value()
    assert title_value == "", \
        f"Title should be empty by default, but was '{title_value}'"

    # 2. Tags
    assert create_news_page.are_tags_visible(), "Tags should be visible"

    selected_tags = create_news_page.get_selected_tags()
    tag_items = create_news_page.tags

    any_selected = any(tag.is_selected() for tag in tag_items)

    assert not any_selected, "No tag should be selected by default"

    assert selected_tags == [], \
        f"Selected tags should be empty by default, but was {selected_tags}"

    # 3. Image Upload
    image_component = create_news_page.image_component

    assert image_component.get_image_input_info() is not None, \
        "Image upload field should be present"
    assert image_component.is_image_field_visible(), \
        "Image field should be visible"
    assert not image_component.is_uploaded_image_present(), \
        "Loaded image should not be present by default"
    assert image_component.is_placeholder_image_present(), \
        "Image zone should be visible"
    assert image_component.is_cancel_cropper_button_visible(), \
        "Cancel button on cropper should be visible"
    assert image_component.is_submit_cropper_button_visible(), \
        "Submit button on cropper should be visible"

    # 4. Source
    assert create_news_page.is_source_visible(), "Source should be visible"

    source_value = create_news_page.get_source()
    assert source_value == "", f"Source field should be empty by default, but was '{source_value}'"

    # 5. Content
    content = create_news_page.content_component

    assert content.is_content_visible(), "Content should be visible"
    assert content.is_content_toolbar_visible(), "Content toolbar should be visible"
    assert content.is_content_counter_visible(), "Content counter should be visible"
    assert content.is_content_message_visible(), "Content message should be visible"

    content_text = content.get_content_text()
    content_counter = content.get_content_counter_text()

    assert content_text == "", f"Content should be empty by default, but was '{content_text}'"
    assert content_counter == "", f"Content counter should be empty by default, but was '{content_counter}'"

    # 6. Author
    assert create_news_page.is_author_visible(), "Author name should be visible"

    author_value = create_news_page.get_author()
    expected_user_from_header = create_news_page.header.get_user()
    expected_test_author = Config.USER_NAME

    assert author_value == expected_user_from_header, \
        f"Author should be pre-filled from header.\nExpected: '{expected_user_from_header}'\nActual: '{author_value}'"

    assert author_value == expected_test_author, \
        f"Author should match test author.\nExpected: '{expected_test_author}'\nActual: '{author_value}'"

    # 7. Date
    assert create_news_page.is_post_date_visible(), "Post date should be visible"

    # 8. Publish, Preview, Cancel buttons
    assert create_news_page.is_cancel_button_visible(), "Cancel button should be visible"
    assert create_news_page.is_preview_button_visible(), "Preview button should be visible"
    assert create_news_page.is_publish_button_visible(), "Publish button should be visible"

    # 9. Language-specifics
    data = CREATE_NEWS_LANGUAGE_DATA[language]

    check.equal(create_news_page.get_all_tags(), data["expected_tags"])
    check.equal(image_component.get_drop_zone_text(), data["drop_zone"])
    check.equal(image_component.get_browse_text(), data["browse"])
    check.equal(image_component.get_cancel_cropper_text(), data["cancel"])
    check.equal(image_component.get_submit_cropper_text(), data["submit"])
    check.equal(image_component.get_image_error(), data["image_error"])
    check.equal(create_news_page.get_source_message_text(), data["source_message"])
    check.equal(create_news_page.get_source_placeholder(), data["source_placeholder"])
    check.equal(content.get_content_message(), data["content_message"])
    check.equal(content.get_content_placeholder(), data["content_placeholder"])
    check.equal(create_news_page.get_post_date(), data["date"])
    check.equal(create_news_page.get_cancel_button_text(), data["cancel_text"])
    check.equal(create_news_page.get_preview_button_text(), data["preview_text"])
    check.equal(create_news_page.get_publish_button_text(), data["publish_text"])

    create_news_page.click_cancel()
    cancel_modal = create_news_page.cancel_modal
    assert cancel_modal.is_visible(), \
        "Confirmation modal should appear after clicking Cancel"
    assert cancel_modal.is_cancel_button_visible(), "'Yes, cancel' button should be visible"
    assert cancel_modal.is_continue_editing_button_visible(), "'Continue editing' button should be visible"

    check.equal(
        cancel_modal.get_warning_title_text(),
        data["modal"]["title"],
        f"Warning title text is incorrect.\nExpected: '{data['modal']['title']}'\nActual: '{cancel_modal.get_warning_title_text()}'"
    )
    check.equal(
        cancel_modal.get_warning_subtitle_text(),
        data["modal"]["subtitle"],
        f"Warning subtitle text is incorrect.\nExpected: '{data['modal']['subtitle']}'\nActual: '{cancel_modal.get_warning_subtitle_text()}'"
    )
    check.equal(
        cancel_modal.get_yes_cancel_button_text(),
        data["modal"]["yes"],
        f"'Yes, cancel' button text is incorrect.\nExpected: '{data['modal']['yes']}'\nActual: '{cancel_modal.get_yes_cancel_button_text()}'"
    )
    check.equal(
        cancel_modal.get_continue_editing_button_text(),
        data["modal"]["continue"],
        f"'Continue editing' button text is incorrect.\nExpected: '{data['modal']['continue']}'\nActual: '{cancel_modal.get_continue_editing_button_text()}'"
    )

    cancel_modal.click_close()
    cancel_modal.wait_until_closed()
    assert create_news_page.is_page_opened(), "User should be redirected to CreateNewsPage"
    current_url = create_news_page.get_current_url()
    assert current_url is not None, "Current URL should not be null"
    assert "/create-news" in current_url, \
        "URL should contain /create-news after closing the cancel modal"

    NewsTestData.apply_to_en(create_news_page) if language == Language.EN else NewsTestData.apply_to_ua(create_news_page)

    preview: NewsPreviewPage = create_news_page.click_preview()
    assert preview.is_page_opened(), "User should be directed to NewsPreviewPage"
    assert preview.is_back_to_create_news_btn_visible(), "Back to editing button should be displayed"
    assert preview.is_public_news_btn_visible(), "Publish button should be displayed"
    assert preview.tags, "Tags list should not be empty on Preview page"

    author_name = preview.get_author_name()
    assert author_name, "Author name should be displayed on Preview page"
    assert preview.is_news_creating_date_visible(), "News creating date should be displayed"
    assert preview.is_image_visible(), "News image input should be displayed on Preview page"
    src = preview.get_preview_image_src()
    assert src is not None, "Preview image src should not be null"
    assert src != "", "Preview image src should not be empty"

    td = data["test_data"]
    check.equal(preview.get_news_title(), td["title"], "News title on Preview page should match entered title")
    check.is_in(td["tags"], preview.get_tag_texts(), f"Preview page should contain tag: {td['tags']}")
    check.equal(preview.get_news_text(), td["content"], "News content on Preview page should match entered content")
    check.equal(preview.get_news_source(), td["source"], "News source on Preview page should match entered source")

    create_news_page = preview.click_back_to_create_news_btn()
    assert create_news_page.is_page_opened_after_preview_click_back(), \
        "User should be redirected to CreateNewsPage after clicking Back button"

    create_news_page.reload()
    assert create_news_page.is_page_opened(), "Create News page should be opened before creating news"

    if language == Language.EN:
        create_news_page.header.change_to_en()
        NewsTestData().apply_to_en(create_news_page)
    else:
        create_news_page.header.change_to_uk()
        NewsTestData().apply_to_ua(create_news_page)
    assert create_news_page.is_publish_button_enabled(), "Publish button should become enabled after all fields are valid."
    create_news_page.click_publish()
    eco_news_page = NewsPage(create_news_page.driver)
    assert eco_news_page.is_page_opened(), "User should be directed to EcoNewsPage"
    if language == Language.EN:
        eco_news_page.header.change_to_en()
        expected_message = "Your news has been successfully published"
    else:
        eco_news_page.header.change_to_uk()
        expected_message = "Ваша новина успішно опублікована"

    assert eco_news_page.get_message_text() == expected_message, "Success message text should be correct"
