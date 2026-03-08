from pathlib import Path
from typing import List

from enums.news_tag import EcoNewsTag
from pages.create_edit_news.create_news_page import CreateNewsPage

TEST_TITLE_EN: str = "Test"
TEST_CONTENT_EN: str = "Test content with 20 chars"
TEST_SOURCE_EN: str = "https://chatgpt.com/"

TEST_TITLE_UA: str = "Tecт"
TEST_CONTENT_UA: str = "Тестовий контент з 30 символів"
TEST_SOURCE_UA: str = "https://claude.ai/"

TEST_TAGS: List[EcoNewsTag] = [EcoNewsTag.NEWS, EcoNewsTag.EVENTS]

ROOT_DIR: Path = Path(__file__).parent.parent
TEST_FILE: Path = (ROOT_DIR / "data/images/test.jfif").resolve()
TEST2_FILE: Path = (ROOT_DIR / "data/images/test2.png").resolve()

TOO_LARGE_IMAGE: Path = (ROOT_DIR / "data/images/UploadImageTest/Andromeda_Galaxy.jpg").resolve()
SMALL_PNG_IMAGE: Path = (ROOT_DIR / "data/images/UploadImageTest/Small PNG.png").resolve()
GIF_IMAGE: Path = (ROOT_DIR / "data/images/UploadImageTest/cactus.gif").resolve()

VALID_CONTENT: str = "This is a valid content with more than 20 characters for the news item."

NEWS_TITLE: str = "Hello World"
NEWS_CONTENT: str = "Description for test news Description for test news"

SOURCE_LINK: str = "hello"
SOURCE_FIELD_ERROR_MESSAGE: str = "Будь ласка, додайте посилання на оригінальну статтю"
TAGS_TO_SELECT: List[str] = [
    EcoNewsTag.NEWS.ua,
    EcoNewsTag.ADS.ua,
    EcoNewsTag.EVENTS.ua,
]

UPDATED_NEWS_TITLE: str = "Test News Updated"

NOT_VALID_CONTENT: str = "Not valid content(("
MODIFIED_TEXT = "Modified text for cancel test"

def apply_to_en(page: CreateNewsPage):
    page.create_news(
        title=TEST_TITLE_EN,
        tags=EcoNewsTag.get_en(TEST_TAGS),
        source=TEST_SOURCE_EN,
        content=TEST_CONTENT_EN,
        image_path=str(TEST_FILE)
    )


def apply_to_ua(page: CreateNewsPage):
    page.create_news(
        title=TEST_TITLE_UA,
        tags=EcoNewsTag.get_ua(TEST_TAGS),
        source=TEST_SOURCE_UA,
        content=TEST_CONTENT_UA,
        image_path=str(TEST2_FILE)
    )
