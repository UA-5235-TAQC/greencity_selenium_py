from enum import Enum
from typing import Optional

from enums.language import Language


class MySpaceTab(Enum):
    """ Enum representing the main tabs in the My Space page. """

    HABITS = ("My habits", "Мої звички")
    NEWS = ("My news", "Мої новини")
    EVENTS = ("My events", "Мої події")

    def __init__(self, en: str, ua: str):
        """ Initialize a MySpaceTab enum member with English and Ukrainian names. """
        self._en = en
        self._ua = ua

    @property
    def en(self) -> str:
        """Return the English name of the tab."""
        return self._en

    @property
    def ua(self) -> str:
        """Return the Ukrainian name of the tab."""
        return self._ua

    def get_by_locale(self, language: Language) -> str:
        """ Return tab name according to selected language. """
        return self._ua if language == Language.UK else self._en

    def matches(self, actual_text: Optional[str]) -> bool:
        """ Check if given text matches either EN or UA value. """
        if not actual_text:
            return False
        normalized = actual_text.strip().lower()
        return normalized in {self._en.lower(), self._ua.lower()}
