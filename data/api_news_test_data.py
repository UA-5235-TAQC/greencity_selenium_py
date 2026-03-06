from dataclasses import dataclass
from typing import List

from enums.news_tag import EcoNewsTag
from models.eco_news_request import EcoNewsRequest
from models.update_eco_news_request import UpdateEcoNewsRequest


@dataclass
class EcoNewsDtoFactory:
    """Factory for creating test EcoNews DTOs in English and Ukrainian."""
    eco_news_id: int

    # Tags for testing
    TEST_TAGS: List[EcoNewsTag] = (EcoNewsTag.NEWS, EcoNewsTag.EDUCATION)

    # English
    TITLE_EN: str = "Welcome to Wikipedia"
    CONTENT_EN: str = ("The Saxe-Goldstein hypothesis is a prediction in archaeology "
                       "about the relationship between a society's funerary practices "
                       "and its social organization.")
    SHORT_INFO_EN: str = "The main page of Wikipedia in English"
    SOURCE_EN: str = "https://en.wikipedia.org/wiki/Main_Page"

    # Ukrainian
    TITLE_UK: str = "Ласкаво просимо до Вікіпедії"
    CONTENT_UK: str = ("Осип Тадейович Назарук (1883 — 1940) — український громадський і "
                       "політичний діяч, письменник, журналіст, воєнний кореспондент, публіцист, "
                       "адвокат.")
    SHORT_INFO_UK: str = "Головна сторінка Вікіпедії українською"
    SOURCE_UK: str = "https://uk.wikipedia.org/wiki/Main_Page"

    def create_news_en(self) -> EcoNewsRequest:
        """Create EcoNewsRequest in English"""
        return EcoNewsRequest(title=self.TITLE_EN, text=self.CONTENT_EN, short_info=self.SHORT_INFO_EN,
            source=self.SOURCE_EN, tags=EcoNewsTag.get_en(self.TEST_TAGS))

    def create_news_uk(self) -> EcoNewsRequest:
        """Create EcoNewsRequest in Ukrainian"""
        return EcoNewsRequest(title=self.TITLE_UK, text=self.CONTENT_UK, short_info=self.SHORT_INFO_UK,
            source=self.SOURCE_UK, tags=EcoNewsTag.get_ua(self.TEST_TAGS))

    def update_dto_en(self) -> UpdateEcoNewsRequest:
        """Create UpdateEcoNewsRequest in English"""
        return UpdateEcoNewsRequest(id=self.eco_news_id, title=self.TITLE_EN, content=self.CONTENT_EN,
            short_info=self.SHORT_INFO_EN, tags=EcoNewsTag.get_en(self.TEST_TAGS), source=self.SOURCE_EN)

    def update_dto_uk(self) -> UpdateEcoNewsRequest:
        """Create UpdateEcoNewsRequest in Ukrainian"""
        return UpdateEcoNewsRequest(id=self.eco_news_id, title=self.TITLE_UK, content=self.CONTENT_UK,
            short_info=self.SHORT_INFO_UK, tags=EcoNewsTag.get_ua(self.TEST_TAGS), source=self.SOURCE_UK)
