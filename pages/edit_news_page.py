from pages.base_page import BasePage


class EditNewsPage(BasePage):

    def __init__(self, driver, news_id: int):
        super().__init__(driver)
        self.news_id = news_id

    def is_page_opened(self) -> bool:
        return True