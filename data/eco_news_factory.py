from dataclasses import dataclass
from typing import List

from enums.news_tag import EcoNewsTag
from models.eco_news_request import EcoNewsRequest
from models.update_eco_news_request import UpdateEcoNewsRequest

# Tags for testing
TEST_TAGS: List[EcoNewsTag] = [EcoNewsTag.NEWS, EcoNewsTag.EDUCATION]  # pylint: disable=C0103

# English
TITLE_EN: str = "Welcome to Wikipedia"  # pylint: disable=C0103
CONTENT_EN: str = "The Saxe-Goldstein hypothesis is a prediction in archaeology "
"about the relationship between a society's funerary practices "
"and its social organization."  # pylint: disable=C0103, W0105

SHORT_INFO_EN: str = "The main page of Wikipedia in English"  # pylint: disable=C0103
SOURCE_EN: str = "https://en.wikipedia.org/wiki/Main_Page"  # pylint: disable=C0103

# Ukrainian
TITLE_UK: str = "Ласкаво просимо до Вікіпедії"  # pylint: disable=C0103
CONTENT_UK: str = "Осип Тадейович Назарук (1883 — 1940) — український громадський і "
"політичний діяч, письменник, журналіст, воєнний кореспондент, публіцист, "
"адвокат."  # pylint: disable=C0103,  W0105
SHORT_INFO_UK: str = "Головна сторінка Вікіпедії українською"  # pylint: disable=C0103
SOURCE_UK: str = "https://uk.wikipedia.org/wiki/Main_Page"  # pylint: disable=C0103


def create_news_en() -> EcoNewsRequest:
    """Create EcoNewsRequest in English"""
    return EcoNewsRequest(title=TITLE_EN, text=CONTENT_EN, short_info=SHORT_INFO_EN,
                          source=SOURCE_EN, tags=EcoNewsTag.get_en(TEST_TAGS))


def create_news_uk() -> EcoNewsRequest:
    """Create EcoNewsRequest in Ukrainian"""
    return EcoNewsRequest(title=TITLE_UK, text=CONTENT_UK, short_info=SHORT_INFO_UK,
                          source=SOURCE_UK, tags=EcoNewsTag.get_ua(TEST_TAGS))


@dataclass
class EcoNewsUpdateFactory:
    """Factory for creating test EcoNews DTOs in English and Ukrainian."""
    eco_news_id: int

    def update_dto_en(self) -> UpdateEcoNewsRequest:
        """Create UpdateEcoNewsRequest in English"""
        return UpdateEcoNewsRequest(id=self.eco_news_id, title=TITLE_EN, content=CONTENT_EN,
                                    short_info=SHORT_INFO_EN, tags=EcoNewsTag.get_en(TEST_TAGS),
                                    source=SOURCE_EN)

    def update_dto_uk(self) -> UpdateEcoNewsRequest:
        """Create UpdateEcoNewsRequest in Ukrainian"""
        return UpdateEcoNewsRequest(id=self.eco_news_id, title=TITLE_UK, content=CONTENT_UK,
                                    short_info=SHORT_INFO_UK, tags=EcoNewsTag.get_ua(TEST_TAGS),
                                    source=SOURCE_UK)
