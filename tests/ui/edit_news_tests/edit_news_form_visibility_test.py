import allure
import pytest_check as check

from data.config import Config
from enums.news_tag import EcoNewsTag
from pages.create_edit_news.edit_news_page import EditNewsPage
from pages.create_edit_news.news_preview_page import NewsPreviewPage
from pages.news_page import NewsPage
from data.language_data import EDIT_NEWS_LANGUAGE_DATA
from tests.utils.merge_tags import merge_tags_unique
from data.ui_news_test_data import NewsTestData
from utils.date_utils import DateUtils


def check_tags(edit_news_page, get_all_tags_fn, test_tags, new_tags, tags_to_select):
    """ Universal function for checking EN or UA tags. """
    assert edit_news_page.are_tags_visible(), "Tags should be visible"
    expected_tags = get_all_tags_fn()
    assert edit_news_page.get_all_tags() == expected_tags, "All tags should match expected"

    actual_tags = edit_news_page.get_selected_tags()
    tag_items = edit_news_page.tags
    any_selected = any(tag.is_selected() for tag in tag_items)
    assert any_selected, "Test tag should be selected by default"
    assert actual_tags == test_tags, "Selected tags do not match expected tags"

    edit_news_page.select_tags(new_tags)
    actual_tags = edit_news_page.get_selected_tags()
    expected_tags = merge_tags_unique(test_tags, new_tags)
    assert len(actual_tags) == len(expected_tags), "Selected tags count mismatch"
    assert actual_tags == expected_tags, "Selected tags do not match expected tags"

    edit_news_page.clear_all_selected_tags().select_tags(tags_to_select)
    actual_tags = edit_news_page.get_selected_tags()
    tag_items = edit_news_page.tags
    any_selected = any(tag.is_selected() for tag in tag_items)
    assert any_selected, "Tags should be selected"
    assert len(actual_tags) == len(tags_to_select), "Selected tags count mismatch"
    assert actual_tags == tags_to_select, "Selected tags do not match expected tags"


@allure.tag("Edit News")
@allure.epic("EcoNews Management")
@allure.feature("Edit news page")
@allure.story("Verify visibility and behavior of Edit News form")
@allure.severity(allure.severity_level.NORMAL)
@allure.issue("14")
@allure.description("Verify that the Create News form contains the particular fields.")
def test_verify_edit_news_form_fields_visibility(edit_news_page_with_language: EditNewsPage):
    """ Verify that the Edit News form contains the particular fields. """
    edit_news_page_with_language.set_window_size(2560, 1440)
    edit_news_page = edit_news_page_with_language
    current_locale = edit_news_page.header.get_current_locale()
    data = EDIT_NEWS_LANGUAGE_DATA[current_locale]

    # 1. Title
    assert edit_news_page.get_title_counter_text() == "4/170"
    assert edit_news_page.get_title_length() == 4
    check.equal(edit_news_page.get_title_value(), data["base_title"])

    # Append
    edit_news_page.append_title(data["to_append"])
    check.equal(edit_news_page.get_title_counter_text(), f"{data['expected_append_len']}/170")
    check.equal(edit_news_page.get_title_length(), data["expected_append_len"])
    check.equal(
        edit_news_page.get_title_value(),
        data["base_title"] + data["to_append"]
    )

    # Prepend
    edit_news_page.prepend_title(data["to_prepend"])
    check.equal(edit_news_page.get_title_counter_text(), f"{data['expected_prepend_len']}/170")
    check.equal(edit_news_page.get_title_length(), data["expected_prepend_len"])
    check.equal(
        edit_news_page.get_title_value(),
        data["to_prepend"] + data["base_title"] + data["to_append"]
    )

    # Remove
    edit_news_page.remove_last_title_chars(data["remove_last"])
    edit_news_page.remove_first_title_chars(data["remove_first"])

    check.equal(edit_news_page.get_title_counter_text(), "4/170")
    check.equal(edit_news_page.get_title_length(), 4)
    check.equal(edit_news_page.get_title_value(), data["base_title"])

    # Enter new title
    test_title = data["to_prepend"] + data["base_title"]
    edit_news_page.enter_title(test_title)

    check.equal(edit_news_page.get_title_counter_text(), f"{data['final_len']}/170")
    check.equal(edit_news_page.get_title_length(), data["final_len"])
    check.equal(edit_news_page.get_title_value(), test_title)

    # 2. Tags
    tags_config = data["tags_config"]
    check_tags(
        edit_news_page,
        get_all_tags_fn=tags_config["get_all"],
        test_tags=tags_config["get_selected"](NewsTestData.TEST_TAGS),
        new_tags=tags_config["get_selected"]([EcoNewsTag.EVENTS, EcoNewsTag.EDUCATION]),
        tags_to_select=tags_config["get_selected"]([EcoNewsTag.INITIATIVES, EcoNewsTag.ADS])
    )

    # 3. Image Upload
    image_component = edit_news_page.image_component
    assert image_component.is_image_visible(), "Image should be visible"
    assert image_component.get_uploaded_image_src() != "", "Image upload field should not be empty"
    assert image_component.is_saved_image_displayed(), "Uploaded image should be present"
    assert image_component.is_uploaded_image_present(), "Uploaded image should be present"
    assert image_component.is_cancel_cropper_button_visible(), "Cancel button on cropper should be visible"
    assert image_component.is_submit_cropper_button_visible(), "Submit button on cropper should be visible"
    check.equal(image_component.get_image_error(), data["image_error"])
    check.equal(image_component.get_cancel_cropper_text(), data["cancel_cropper"])
    check.equal(image_component.get_submit_cropper_text(), data["submit_cropper"])

    image_component = image_component.change_image(NewsTestData.TEST2_FILE)

    assert image_component.is_preview_image_visible(), "Preview image should be visible"
    assert image_component.get_preview_image_src() != "", "Preview image src should not be empty"
    assert image_component.is_preview_image_present(), "Preview image should be present after crop submit"
    assert image_component.is_cancel_cropper_button_visible(), "Cancel button on cropper should be visible after change"
    assert image_component.is_submit_cropper_button_visible(), "Submit button on cropper should be visible after change"

    # 4. Source
    assert edit_news_page.is_source_visible(), "Source should be visible"

    source = edit_news_page.get_source()
    assert source == "", "Expected the Source field to be empty due to an application issue"
    check.not_equal(
        source,
        data["test_source"],
        "Source field should not retain the previously entered test source due to an application issue"
    )
    check.equal(edit_news_page.get_source_message_text(), data["source_message"])

    # 5. Content
    content = edit_news_page.content_component
    assert content.is_content_visible(), "Content should be visible"
    assert content.is_content_toolbar_visible(), "Content toolbar should be visible"
    assert content.is_content_counter_visible(), "Content counter should be visible"
    assert content.is_content_message_visible(), "Content message should be visible"
    check.equal(
        content.get_content_text(),
        data["test_content"],
        "Content should be the same as test content"
    )

    # Append
    content.enter_content_not_clear(data["to_append"])
    assert content.is_content_valid(), "Content is invalid after append"
    check.equal(
        content.get_content_counter_text(),
        data["content_counter_after_append"],
        "Content counter after append is incorrect"
    )
    check.equal(
        content.get_actual_content_length(),
        data["content_length_after_append"],
    )
    check.equal(
        content.get_content_text(),
        data["test_content"] + data["to_append"],
        "Content should be appended"
    )

    # Prepend
    content.prepend_content(data["to_prepend"])
    assert content.is_content_valid(), "Content is invalid after prepend"
    check.equal(
        content.get_content_counter_text(),
        data["content_counter_after_prepend"],
    )
    check.equal(
        content.get_actual_content_length(),
        data["content_length_after_prepend"],
    )
    check.equal(
        content.get_content_text(),
        data["to_prepend"] + data["test_content"] + data["to_append"],
        "Content should be prepended"
    )

    # Remove
    content.remove_last_content_chars(data["remove_last"])
    content.remove_first_content_chars(data["remove_first"])
    check.equal(
        content.get_content_counter_text(),
        data["content_counter_after_remove"],
    )
    check.equal(
        content.get_actual_content_length(),
        data["content_length_after_remove"],
    )
    check.equal(
        content.get_content_text(),
        data["test_content"],
        "Content should return to initial test content"
    )

    # Clear
    content.clear_content()
    assert content.is_content_visible()
    assert content.is_content_toolbar_visible()
    assert content.is_content_counter_visible()
    assert content.is_content_message_visible()
    check.is_false(content.is_content_valid())
    check.is_true(content.is_content_invalid())
    check.equal(content.get_content_text(), "")
    check.equal(content.get_content_counter_text(), "")
    check.is_true(content.is_content_message_visible())
    check.is_true(content.is_content_message_invalid())
    check.is_true(content.is_content_warning_displayed())
    check.equal(
        content.get_content_placeholder(),
        data["content_placeholder"],
        "Incorrect content placeholder text"
    )
    check.equal(
        content.get_content_message(),
        data["content_message"],
        "Incorrect content validation message"
    )

    # Final combined string
    test_string = data["base_title"] + " " + data["test_content"]
    content.enter_content(test_string)
    check.equal(
        content.get_content_counter_text(),
        data["content_counter_final"],
    )
    check.equal(
        content.get_actual_content_length(),
        data["content_length_final"],
    )
    check.equal(
        content.get_content_text(),
        test_string
    )

    # 6. Author
    assert edit_news_page.is_author_visible(), "Author name should be visible"
    check.equal(
        edit_news_page.get_author(),
        edit_news_page.header.get_user(),
        "Author should be pre-filled"
    )
    expected_test_author = Config.USER_NAME
    check.equal(
        edit_news_page.get_author(),
        expected_test_author,
        "Author should be the test author"
    )

    # 7. Date
    assert edit_news_page.is_post_date_visible(), "Post date should be visible"
    expected_date = DateUtils.get_current_date_formatted(current_locale)
    check.equal(
        edit_news_page.get_post_date(),
        expected_date,
        "Date should be today's date"
    )

    # 8. Publish, Preview, Cancel buttons
    assert edit_news_page.is_cancel_button_visible(), "Cancel button should be visible"
    assert edit_news_page.is_preview_button_visible(), "Preview button should be visible"
    assert edit_news_page.is_edit_button_visible(), "Publish button should be visible"
    check.equal(
        edit_news_page.get_cancel_button_text(),
        data["cancel_button_text"],
        "Cancel button text is incorrect"
    )
    check.equal(
        edit_news_page.get_preview_button_text(),
        data["preview_button_text"],
        "Preview button text is incorrect"
    )
    check.equal(
        edit_news_page.get_edit_button_text(),
        data["edit_button_text"],
        "Edit button text is incorrect"
    )
    eco_news_id = edit_news_page.get_id()

    # 9. Cancel modal
    edit_news_page.click_cancel()
    cancel_modal = edit_news_page.cancel_modal
    assert cancel_modal.is_visible(), "Confirmation modal should appear after clicking Cancel"
    assert cancel_modal.is_cancel_button_visible(), "'Yes, cancel' button should be visible"
    assert cancel_modal.is_continue_editing_button_visible(), "'Continue editing' button should be visible"

    check.equal(
        cancel_modal.get_warning_title_text(),
        data["cancel_modal_warning_title"],
        "Warning title text is incorrect"
    )
    check.equal(
        cancel_modal.get_warning_subtitle_text(),
        data["cancel_modal_warning_subtitle"],
        "Warning subtitle text is incorrect"
    )
    check.equal(
        cancel_modal.get_yes_cancel_button_text(),
        data["cancel_modal_yes_button"],
        "'Yes, cancel' button text is incorrect"
    )
    check.equal(
        cancel_modal.get_continue_editing_button_text(),
        data["cancel_modal_continue_button"],
        "'Continue editing' button text is incorrect"
    )

    # Close modal and wait until closed
    cancel_modal.click_close()
    cancel_modal.wait_until_closed()

    # Verify user is back on Create News page
    assert edit_news_page.is_page_opened(), "User should be redirected to CreateNewsPage"
    current_url = edit_news_page.get_current_url()
    assert current_url is not None, "Current URL should not be null"
    assert "/create-news" in current_url, "URL should contain /create-news after closing the cancel modal"

    # 10. News Preview
    edit_news_page.edit_news(
        title=data["title"],
        tags=data["tags"],
        source=data["source"],
        content=data["content"],
        image_path=data["image_file"]
    )
    preview: NewsPreviewPage = edit_news_page.click_preview()
    assert preview.is_page_opened(), "User should be directed to NewsPreviewPage"
    assert preview.is_back_to_create_news_btn_visible(), "Back to Create News button should be displayed"
    assert preview.is_public_news_btn_visible(), "Publish News button should be displayed"
    check.equal(preview.get_news_title(), data["title"],
                "News title on Preview page should match entered title")
    preview_tags = preview.get_tag_texts()
    assert preview_tags, "Tags list should not be empty on Preview page"
    check.equal(sorted(preview_tags), sorted(data["tags"]), "Tags on Preview page should match entered tags")
    check.equal(preview.get_news_source(), data["source"],
                "News source on Preview page should match entered source")
    check.equal(preview.get_news_text(), data["content"],
                "News content on Preview page should match entered content")
    assert preview.is_author_name_visible(), "News author name should be displayed"
    author_name = preview.get_author_name()
    assert author_name, "Author name should be displayed on Preview page"
    assert preview.is_news_creating_date_visible(), "News creating date should be displayed"
    assert preview.is_image_visible(), "News image should be displayed on Preview page"
    src = preview.get_preview_image_src()
    assert src is not None, "Preview image src should not be null"
    assert src != "", "Preview image src should not be empty"

    # 11. Edit News
    edit_news_page = preview.back_to_editing(eco_news_id)
    assert edit_news_page.is_page_opened_after_preview_click_back(), \
        "User should be redirected to CreateNewsPage after clicking Back button"
    edit_news_page.reload()
    assert edit_news_page.is_page_opened(), "Create News page should be opened before creating news"
    edit_news_page.edit_news(
        title=data["edit_title"],
        tags=data["edit_tags"],
        source=data["edit_source"],
        content=data["edit_content"],
        image_path=data["edit_image_file"]
    )
    assert edit_news_page.is_edit_button_enabled(), "Edit button should become enabled after all fields are valid"
    edit_news_page.click_edit()
    eco_news_page = NewsPage(edit_news_page.driver)
    assert eco_news_page.is_page_opened(), "User should be directed to EcoNews page"
    success_message = eco_news_page.get_message_text()
    check.equal(success_message, data["success_message"], "Success message text should be correct")
