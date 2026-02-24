from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.base_component import BaseComponent


class ProfilePanelComponent(BaseComponent):
    """
    Represents the Profile Panel component in the GreenCity UI.
    Provides access to the user's avatar, name, location, rate,
    achievements, friends count, eco places, and allows adding a friend.
    """

    AVATAR = (By.CSS_SELECTOR, "app-user-profile-image img.profile-avatar")
    NAME = (By.CSS_SELECTOR, "app-profile-header p.name")
    LOCATION = (By.CSS_SELECTOR, "p.location")
    RATE = (By.CSS_SELECTOR, "div.rate p")
    ACHIEVEMENTS = (By.CSS_SELECTOR, "app-users-achievements .achievements-images img")
    FRIENDS_COUNT_LABEL = (By.CSS_SELECTOR, "app-users-friends .text-number")
    FAVOURITE_PLACES = (By.CSS_SELECTOR, "app-eco-places .eco-place-list li")
    ADD_FRIEND_BUTTON = (By.CSS_SELECTOR, "app-users-friends .add-friends a")

    @allure.step("Get user avatar element")
    def get_avatar(self) -> WebElement:
        """Return the avatar WebElement."""
        return self.find(self.AVATAR)

    @allure.step("Get user full name")
    def get_name(self) -> str:
        """Return the full name of the user."""
        return self.get_text(self.NAME)

    @allure.step("Get user location")
    def get_location(self) -> str:
        """Return the location of the user."""
        return self.get_text(self.LOCATION)

    @allure.step("Get user rate")
    def get_rate(self) -> int:
        """Return the user's rate as integer."""
        return self.get_int_from_text(self.RATE)

    @allure.step("Get user achievements list")
    def get_achievements(self) -> List[WebElement]:
        """Return the list of achievement WebElements."""
        elements = self.find_all(self.ACHIEVEMENTS)
        return elements if elements else []

    @allure.step("Get friends count")
    def get_friends_count(self) -> int:
        """Return the number of friends displayed in the UI."""
        return self.get_int_from_text(self.FRIENDS_COUNT_LABEL, part_index=0)

    @allure.step("Click add friend button")
    def add_friend(self):
        """Click the add friend button."""
        self.click(self.ADD_FRIEND_BUTTON)

    @allure.step("Get favourite eco places list")
    def get_favourite_places(self) -> List[WebElement]:
        """Return the list of favourite eco places."""
        elements = self.find_all(self.FAVOURITE_PLACES)
        return elements if elements else []
