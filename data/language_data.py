from enums.language import Language
from enums.news_tag import EcoNewsTag
from utils.date_utils import DateUtils
from data.ui_news_test_data import NewsTestData

CREATE_NEWS_LANGUAGE_DATA = {
    Language.EN: {
        "expected_tags": EcoNewsTag.get_all_en(),
        "drop_zone": "Drop your image here or",
        "browse": "browse",
        "cancel": "Cancel",
        "submit": "Submit",
        "image_error": "Upload only PNG or JPG. File size must be less than 10MB",
        "source_message": (
            "Source (optional)\n"
            "Please add the link of original article/news/post. Link must start with http(s)://"
        ),
        "source_placeholder": "Link to external source",
        "content_message": "Must be minimum 20 and maximum 63 206 symbols",
        "content_placeholder": "e.g. Short description of news, agenda for event",
        "date": DateUtils.get_current_date_formatted(Language.EN),
        "cancel_text": "Cancel",
        "preview_text": "Preview",
        "publish_text": "Publish",
        "modal": {
            "title": "All created content will be lost.",
            "subtitle": "Do you still want to cancel news creating?",
            "yes": "Yes, cancel",
            "continue": "Continue editing"
        },
        "test_data": {
            "title": NewsTestData.TEST_TITLE_EN,
            "content": NewsTestData.TEST_CONTENT_EN,
            "source": NewsTestData.TEST_SOURCE_EN,
            "tags": EcoNewsTag.get_en(NewsTestData.TEST_TAGS)[0]
        }
    },
    Language.UK: {
        "expected_tags": EcoNewsTag.get_all_ua(),
        "drop_zone": "Перетягніть зображення сюди або",
        "browse": "огляд",
        "cancel": "Скасувати",
        "submit": "Застосувати",
        "image_error": "Завантажуйте лише PNG або JPEG. Розмір файлу не повинен перевищувати 10Mb",
        "source_message": (
            "Джерело (не обов'язково)\n"
            "Будь ласка, додайте посилання на оригінальну статтю/новину/публікацію. "
            "Посилання повинно починатись з http(s)://"
        ),
        "source_placeholder": "Посилання на зовнішнє джерело",
        "content_message": "Поле повинно містити не менше 20 та не більше 63 206 символів",
        "content_placeholder": "напр. Короткий опис новини, план заходу",
        "date": DateUtils.get_current_date_formatted(Language.UK),
        "cancel_text": "Вийти",
        "preview_text": "Переглянути",
        "publish_text": "Опублікувати",
        "modal": {
            "title": "Внесені зміни будуть втрачені.",
            "subtitle": "Ви впевнені, що хочете видалити новину?",
            "yes": "Скасувати",
            "continue": "Продовжити"
        },
        "test_data": {
            "title": NewsTestData.TEST_TITLE_UA,
            "content": NewsTestData.TEST_CONTENT_UA,
            "source": NewsTestData.TEST_SOURCE_UA,
            "tags": EcoNewsTag.get_ua(NewsTestData.TEST_TAGS)[0]
        }
    }
}

EDIT_NEWS_LANGUAGE_DATA = {
    Language.EN: {
        # ---------- Title ----------
        "base_title": NewsTestData.TEST_TITLE_EN,
        "to_append": " New",
        "to_prepend": "Add ",
        "expected_append_len": 8,
        "expected_prepend_len": 12,
        "remove_last": 4,
        "remove_first": 4,
        "final_len": 8,

        # ---------- Image ----------
        "image_error": "Upload only PNG or JPG. File size must be less than 10MB",
        "cancel_cropper": "Cancel",
        "submit_cropper": "Submit",

        # ---------- Source ----------
        "source_message": (
            "Source (optional)\n"
            "Please add the link of original article/news/post. "
            "Link must start with http(s)://"
        ),
        "source_placeholder": "Link to external source",
        "test_source": NewsTestData.TEST_SOURCE_EN,

        # ---------- Content ----------
        "test_content": NewsTestData.TEST_CONTENT_EN,
        "content_placeholder": "e.g. Short description of news, agenda for event",
        "content_message": "Must be minimum 20 and maximum 63 206 symbols",

        "content_counter_after_append": "Number of characters: 30",
        "content_length_after_append": 30,

        "content_counter_after_prepend": "Number of characters: 34",
        "content_length_after_prepend": 34,

        "content_counter_after_remove": "Number of characters: 26",
        "content_length_after_remove": 26,

        "content_counter_final": "Number of characters: 31",
        "content_length_final": 31,

        # ---------- Tags ----------
        "tags_config": {
            "get_all": EcoNewsTag.get_all_en,
            "get_selected": EcoNewsTag.get_en,
        },

        # ---------- Author / Date ----------
        "date_locale": "en_US.UTF-8",
        "date_format": "%b %d, %Y",

        # ---------- Publish, Preview, Cancel buttons ----------
        "cancel_button_text": "Cancel",
        "preview_button_text": "Preview",
        "edit_button_text": "Edit",

        # ---------- Cancel Modal ----------
        "cancel_modal_warning_title": "All created content will be lost.",
        "cancel_modal_warning_subtitle": "Do you still want to cancel news creating?",
        "cancel_modal_yes_button": "Yes, cancel",
        "cancel_modal_continue_button": "Continue editing",

        # ---------- Edit News Preview ----------
        "title": "Max",
        "tags": EcoNewsTag.get_en([EcoNewsTag.INITIATIVES, EcoNewsTag.EVENTS]),
        "source": "https://en.wikipedia.org/wiki/Main_Page",
        "content": "Mount Edziza is a volcanic mountain in Cassiar Land District in northwestern British Columbia, Canada.",
        "image_file": NewsTestData.TEST2_FILE,

        # ---------- Edit News ----------
        "edit_title": NewsTestData.TEST_TITLE_EN,
        "edit_tags": EcoNewsTag.get_en(NewsTestData.TEST_TAGS),
        "edit_source": NewsTestData.TEST_SOURCE_EN,
        "edit_content": NewsTestData.TEST_CONTENT_EN,
        "edit_image_file": NewsTestData.TEST_FILE,

        # ---------- Success message ----------
        "success_message": "Your news has been successfully published"
    },

    Language.UK: {
        # ---------- Title ----------
        "base_title": NewsTestData.TEST_TITLE_UA,
        "to_append": " Новий",
        "to_prepend": "Додати ",
        "expected_append_len": 10,
        "expected_prepend_len": 17,
        "remove_last": 6,
        "remove_first": 7,
        "final_len": 11,

        # ---------- Image ----------
        "image_error": "Завантажуйте лише PNG або JPEG. Розмір файлу не повинен перевищувати 10Mb",
        "cancel_cropper": "Скасувати",
        "submit_cropper": "Застосувати",

        # ---------- Source ----------
        "source_message": (
            "Джерело (не обов'язково)\n"
            "Будь ласка, додайте посилання на оригінальну статтю/новину/публікацію. "
            "Посилання повинно починатись з http(s)://"
        ),
        "source_placeholder": "Посилання на зовнішнє джерело",
        "test_source": NewsTestData.TEST_SOURCE_UA,

        # ---------- Content ----------
        "test_content": NewsTestData.TEST_CONTENT_UA,
        "content_placeholder": "напр. Короткий опис новини, план заходу",
        "content_message": "Поле повинно містити не менше 20 та не більше 63 206 символів",

        "content_counter_after_append": "Кількість символів: 36",
        "content_length_after_append": 36,

        "content_counter_after_prepend": "Кількість символів: 43",
        "content_length_after_prepend": 43,

        "content_counter_after_remove": "Кількість символів: 30",
        "content_length_after_remove": 30,

        "content_counter_final": "Кількість символів: 35",
        "content_length_final": 35,

        # ---------- Tags ----------
        "tags_config": {
            "get_all": EcoNewsTag.get_all_ua,
            "get_selected": EcoNewsTag.get_ua,
        },

        # ---------- Author / Date ----------
        "date_locale": "uk_UA.UTF-8",
        "date_format": "%b %d, %Y р.",

        # ---------- Publish, Preview, Cancel buttons ----------
        "cancel_button_text": "Вийти",
        "preview_button_text": "Переглянути",
        "edit_button_text": "Редагувати",

        # ---------- Cancel Modal ----------
        "cancel_modal_warning_title": "Внесені зміни будуть втрачені.",
        "cancel_modal_warning_subtitle": "Ви впевнені, що хочете видалити новину?",
        "cancel_modal_yes_button": "Скасувати",
        "cancel_modal_continue_button": "Продовжити",

        # ---------- Edit News Preview ----------
        "title": "Макс",
        "tags": EcoNewsTag.get_ua([EcoNewsTag.INITIATIVES, EcoNewsTag.EVENTS]),
        "source": "https://en.wikipedia.org/wiki/Main_Page",
        "content": "Гора Едзіза — вулканічна гора в окрузі Кассіар-Ленд на північному заході Британської Колумбії , Канада.",
        "image_file": NewsTestData.TEST_FILE,

        # ---------- Edit News ----------
        "edit_title": NewsTestData.TEST_TITLE_UA,
        "edit_tags": EcoNewsTag.get_ua(NewsTestData.TEST_TAGS),
        "edit_source": NewsTestData.TEST_SOURCE_UA,
        "edit_content": NewsTestData.TEST_CONTENT_UA,
        "edit_image_file": NewsTestData.TEST2_FILE,

        # ---------- Success message ----------
        "success_message": "Ваша новина успішно опублікована"
    }
}
