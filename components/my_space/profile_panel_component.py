from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import allure
from components.base_component import BaseComponent
from utils.page_factory import LocatorsTable
from utils.web_element_utils import get_int_from_text


class ProfilePanelComponent(BaseComponent):
    """
    Represents the Profile Panel component in the GreenCity UI.
    Provides access to the user's avatar, name, location, rate,
    achievements, friends count, eco places, and allows adding a friend.
    """

    avatar: WebElement
    name: WebElement
    location: WebElement
    rate: WebElement
    achievements: List[WebElement]
    friends_count_label: WebElement
    favourite_places: List[WebElement]
    add_friend_btn: WebElement

    locators: LocatorsTable = {
        "avatar": (By.CSS_SELECTOR, "app-user-profile-image img.profile-avatar"),
        "name": (By.CSS_SELECTOR, "app-profile-header p.name"),
        "location": (By.CSS_SELECTOR, "p.location"),
        "rate": (By.CSS_SELECTOR, "div.rate p"),
        "achievements": (By.CSS_SELECTOR, "app-users-achievements .achievements-images img", List[WebElement]),
        "friends_count_label": (By.CSS_SELECTOR, "app-users-friends .text-number"),
        "favourite_places": (By.CSS_SELECTOR, "app-eco-places .eco-place-list li", List[WebElement]),
        "add_friend_btn": (By.CSS_SELECTOR, "app-users-friends .add-friends a")
    }

    @allure.step("Get user full name")
    def get_name(self) -> str:
        """Return the full name of the user."""
        return self.name.text

    @allure.step("Get user location")
    def get_location(self) -> str:
        """Return the location of the user."""
        return self.location.text

    @allure.step("Get user rate")
    def get_rate(self) -> int:
        """Return the user's rate as integer."""
        return get_int_from_text(self.rate)

    @allure.step("Get friends count")
    def get_friends_count(self) -> int:
        """Return the number of friends displayed in the UI."""
        return get_int_from_text(self.friends_count_label, part_index=0)

    @allure.step("Click add friend button")
    def add_friend(self):
        """Click the add friend button."""
        self.add_friend_btn.click()
