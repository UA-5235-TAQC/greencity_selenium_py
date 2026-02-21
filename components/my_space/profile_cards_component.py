from typing import List

import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class ProfileCardsComponent(BaseComponent):
    """
    Component representing the profile cards section on the MySpace page.
    Each card displays information such as "Fact of the Day" and may include a title, description, and decorative image.
    """

    CARDS_CONTAINER = (By.CSS_SELECTOR, ".right-cards")
    CARDS = (By.CSS_SELECTOR, ".right-cards .card")
    CARD_TITLES = (By.CSS_SELECTOR, ".right-cards .card .cart-title")
    CARD_DESCRIPTIONS = (By.CSS_SELECTOR, ".right-cards .card .card-description")
    CARD_IMAGES = (By.CSS_SELECTOR, ".right-cards .card .shape-img img")

    @allure.step("Get all profile card titles")
    def get_card_titles(self) -> List[str]:
        """Return all profile card titles."""
        return self.get_texts_from(self.CARD_TITLES)

    @allure.step("Get all profile card descriptions")
    def get_card_descriptions(self) -> List[str]:
        """Return all profile card descriptions."""
        return self.get_texts_from(self.CARD_DESCRIPTIONS)

    @allure.step("Get profile card title at index {index}")
    def get_card_title(self, index: int) -> str:
        """Return profile card title by index."""
        return self.get_text_by_index(self.get_card_titles(), index, "card titles")

    @allure.step("Get profile card description at index {index}")
    def get_card_description(self, index: int) -> str:
        """Return profile card description by index."""
        return self.get_text_by_index(self.get_card_descriptions(), index, "card descriptions")

    @allure.step("Get count of profile cards")
    def get_cards_count(self) -> int:
        """ Return the number of visible profile cards. """
        return len(self.find_all(self.CARDS))

    @allure.step("Check if profile cards component is visible")
    def is_displayed(self) -> bool:
        """ Return True if the profile cards component is visible. """
        return self.is_visible(self.CARDS_CONTAINER)
