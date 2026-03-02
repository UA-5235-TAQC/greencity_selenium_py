import os
from pathlib import Path

from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage


class NewsTestData:
    TEST_TITLE_EN = "Test"
    TEST_CONTENT_EN = "Test content with 20 chars"
    TEST_SOURCE_EN = "https://chatgpt.com/"

    TEST_TITLE_UA = "Tecт"
    TEST_CONTENT_UA = "Тестовий контент з 30 символів"
    TEST_SOURCE_UA = "https://claude.ai/"

    TEST_TAGS = [EcoNewsTag.NEWS, EcoNewsTag.EVENTS]

    ROOT_DIR = Path(__file__).parent.parent.parent
    TEST_FILE = (ROOT_DIR / "tests/images/test.jfif").resolve()
    TEST2_FILE = (ROOT_DIR / "tests/images/test2.png").resolve()

    TOO_LARGE_IMAGE = (ROOT_DIR / "tests/images/UploadImageTest/Andromeda_Galaxy.jpg").resolve()
    SMALL_PNG_IMAGE = (ROOT_DIR / "tests/images/UploadImageTest/Small PNG.png").resolve()
    GIF_IMAGE = (ROOT_DIR / "tests/images/UploadImageTest/cactus.gif").resolve()

    VALID_CONTENT = "This is a valid content with more than 20 characters for the news item."

    @staticmethod
    def apply_to_en(page: CreateNewsPage):
        page.create_news(
            title=NewsTestData.TEST_TITLE_EN,
            tags=EcoNewsTag.get_en(NewsTestData.TEST_TAGS),
            source=NewsTestData.TEST_SOURCE_EN,
            content=NewsTestData.TEST_CONTENT_EN,
            image_path=str(NewsTestData.TEST_FILE)
        )

    @staticmethod
    def apply_to_ua(page: CreateNewsPage):
        page.create_news(
            title=NewsTestData.TEST_TITLE_UA,
            tags=EcoNewsTag.get_ua(NewsTestData.TEST_TAGS),
            source=NewsTestData.TEST_SOURCE_UA,
            content=NewsTestData.TEST_CONTENT_UA,
            image_path=str(NewsTestData.TEST2_FILE)
        )
