import locale
from datetime import datetime
import allure

from enums.language import Language


class DateUtils:
    """ Utility class for getting the current date in different formats. """

    @staticmethod
    @allure.step("Get current date in English {lang}")
    def get_current_date_formatted(lang: Language) -> str:
        """ Returns the current date in English or Ukrainian. """
        if lang == Language.EN:
            locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
            return datetime.now().strftime("%b %d, %Y").replace(" 0", " ")
        locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
        raw_date = datetime.now().strftime("%b %d, %Y р.").replace(" 0", " ")
        month, rest = raw_date.split(' ', 1)
        month = month.lower()
        if not month.endswith('.'):
            month += '.'
        return f"{month} {rest}"
