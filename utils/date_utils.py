from datetime import datetime

class DateUtils:
    
    @staticmethod
    def get_current_date_formatted() -> str:
        """  Returns the current date in the format: 'Feb 27, 2026'   """
        return datetime.now().strftime("%b %d, %Y").replace(" 0", " ")