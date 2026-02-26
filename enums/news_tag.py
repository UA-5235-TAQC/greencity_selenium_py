from enum import Enum
from typing import List, Optional

from enums.language import Language


class EcoNewsTag(Enum):
    """ Enum representing tags for Eco News items in English and Ukrainian. """

    NEWS = ("News", "Новини")
    EVENTS = ("Events", "Події")
    EDUCATION = ("Education", "Освіта")
    INITIATIVES = ("Initiatives", "Ініціативи")
    ADS = ("Ads", "Реклама")

    def __init__(self, en: str, ua: str):
        """ Initialize a tag with English and Ukrainian names. """
        self._en = en
        self._ua = ua

    def get_by_locale(self, locale: Language) -> str:
        """ Return the tag name according to the locale. """
        return self._ua if locale == Language.UK else self._en

    @property
    def en(self) -> str:
        """ Return English name of the tag. """
        return self._en

    @property
    def ua(self) -> str:
        """ Return Ukrainian name of the tag. """
        return self._ua

    @classmethod
    def get_all_by_locale(cls, locale: Language) -> List[str]:
        """ Return all tag names for a given locale. """
        return [tag.get_by_locale(locale) for tag in cls]

    @classmethod
    def get_all_en(cls) -> List[str]:
        """ Return all tag names in English. """
        return cls.get_all_by_locale(Language.EN)

    @classmethod
    def get_all_ua(cls) -> List[str]:
        """ Return all tag names in Ukrainian. """
        return cls.get_all_by_locale(Language.UK)

    @classmethod
    def get_by_locale_list(cls, tags: List["EcoNewsTag"], locale: Language) -> List[str]:
        """ Return a list of localized names for the given list of tags. """
        return [tag.get_by_locale(locale) for tag in tags]

    @classmethod
    def get_en(cls, tags: List["EcoNewsTag"]) -> List[str]:
        """ Return a list of English names for the given list of tags. """
        return cls.get_by_locale_list(tags, Language.EN)

    @classmethod
    def get_ua(cls, tags: List["EcoNewsTag"]) -> List[str]:
        """ Return a list of Ukrainian names for the given list of tags. """
        return cls.get_by_locale_list(tags, Language.UK)

    @classmethod
    def map_strings_to_locale(cls, tag_strings: Optional[List[str]], locale: Language) -> List[str]:
        """ Map a list of strings (English or Ukrainian) to localized names. """
        if not tag_strings:
            return []

        result = []
        for value in tag_strings:
            matched_tag = next(
                (tag for tag in cls if tag.en.lower() == value.lower() or tag.ua.lower() == value.lower()),
                None
            )
            if matched_tag:
                result.append(matched_tag.get_by_locale(locale))
        return result
