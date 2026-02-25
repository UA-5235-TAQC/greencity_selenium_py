from enum import Enum


class Language(Enum):
    """ Enum representing supported languages/locales in the application. """

    EN = "En"
    UK = "Uk"

    @property
    def locale_code(self) -> str:
        """Return normalized locale code."""
        return self.name.lower()
