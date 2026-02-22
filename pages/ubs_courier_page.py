from pages.base_page import BasePage


class UbsCourierPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_page_opened(self) -> bool:
        return True