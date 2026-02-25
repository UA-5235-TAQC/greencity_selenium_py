import allure
from typing import List
from utils.page_factory import LocatorsTable, By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent
from components.news_card_component import NewsCardComponent 

class NewsDetailsContentComponent(BaseComponent):
    """
    Component representing the recommended news section (widget).
    Contains a title and a list of news cards.
    """
    title_element: WebElement
    news_cards: List[WebElement]

    locators: LocatorsTable = {
        "title_element": (By.CSS_SELECTOR, ".wrapper p"),
        "news_cards": (By.CSS_SELECTOR, "app-news-list-gallery-view"), 
    }

    @allure.step("Get title text of recommended news section")
    def get_title_text(self) -> str:
        """Return the header text of the recommended news widget."""
        return self.title_element.text

    @allure.step("Get all recommended news cards")
    def get_all_cards(self) -> List[NewsCardComponent]:
        """Find all news card elements and wrap them into NewsCardComponent objects."""
        card_elements = self.root_element.find_elements(*self.locators["news_cards"][:2])
        return [NewsCardComponent(card_el) for card_el in card_elements]

    @allure.step("Get recommended card by index: {index}")
    def get_card_by_index(self, index: int)-> NewsCardComponent:
        """
        Return a NewsCardComponent at the specified index.
        
        Args:
            index: The zero-based index of the card.
        """
        cards = self.get_all_cards()
        if 0 <= index < len(cards):
            return cards[index]
        raise IndexError(f"Card with index {index} is not found. Total cards: {len(cards)}")