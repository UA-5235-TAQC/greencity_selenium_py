from enum import Enum


class Language(Enum):
    EN = "En"
    UK = "Uk"

    @property
    def locale_code(self) -> str:
        """Return normalized locale code."""
        return self.name.lower()
