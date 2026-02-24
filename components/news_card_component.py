import allure
from components.base_component import BaseComponent

class NewsCardComponent(BaseComponent):

    @allure.step("Click on news card")
    def click(self):
        self.root.click()

    @allure.step("Get title of news card")
    def get_title(self) -> str:
        return "There is just some title for test"