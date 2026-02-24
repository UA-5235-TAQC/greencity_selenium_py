import allure
from selenium.webdriver.common.by import By
from components.base_component import BaseComponent
from components.news_card_component import NewsCardComponent 

class NewsDetailsContentComponent(BaseComponent):
    title_locator = (By.CSS_SELECTOR, "app-eco-news-widget .wrapper p") 
    news_card_locator = (By.CSS_SELECTOR, ".list-gallery") 

    @allure.step("Get title text of recommended news section")
    def get_title_text(self) -> str:
        return self.root.find_element(*self.title_locator).text

    @allure.step("Get all recommended news cards")
    def get_all_cards(self):
        card_elements = self.root.find_elements(*self.news_card_locator)
        return [NewsCardComponent(card_el) for card_el in card_elements]

    @allure.step("Get recommended card by index: {index}")
    def get_card_by_index(self, index: int):
        cards = self.get_all_cards()
        if 0 <= index < len(cards):
            return cards[index]
        raise IndexError(f"Card with index {index} is not found.")