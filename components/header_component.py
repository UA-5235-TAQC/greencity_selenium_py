from __future__ import annotations

from typing import Tuple

from selenium.webdriver.common.by import By
from components.auth_modal.sign_in_modal import SignInModal
from components.auth_modal.sign_up_modal import SignUpModal
from components.base_component import BaseComponent
from selenium.webdriver.support import expected_conditions as EC
import allure

from enums.language import Language


class HeaderComponent(BaseComponent):
    """ Represents the header section of the GreenCity application. """
    logo_locator = (By.CSS_SELECTOR, 'a.header_logo')
    news_link_locator = (By.XPATH, "//a[contains(@href, '#/greenCity/news')]")
    my_space_link_locator = (By.XPATH, "//a[contains(@href, '#/greenCity/profile')]")
    sign_in_locator = (By.CSS_SELECTOR, "a.header_sign-in-link")
    sign_up_locator = (By.CSS_SELECTOR, "li.header_sign-up-link")
    search_btn_locator = (By.CSS_SELECTOR, "li.search-icon")
    language_dropdown_locator = (By.CSS_SELECTOR, "ul.header_lang-switcher-wrp")
    user_name_locator = (By.CSS_SELECTOR, ".body-2")
    user_dropdown_locator = (By.CSS_SELECTOR, "ul.dropdown-list")

    @allure.step("Click header logo")
    def click_logo(self) -> "HomePage":
        """ Click on the logo in the header to navigate to the home page. """
        self.click(self.logo_locator)
        from pages.home_page import HomePage
        return HomePage(self.get_driver())

    def wait_until_url_contains(self, value: str):
        """Wait until current URL contains given value."""
        self.wait.until(EC.url_contains(value))

    @allure.step("Click 'Eco News' link in header")
    def click_news_link(self) -> "NewsPage":
        """ Click on the news link in the header to navigate to the Eco News page. """
        self.click(self.news_link_locator)
        from pages.news_page import NewsPage
        return NewsPage(self.get_driver()).wait_until_opened()

    @allure.step("Click 'Sign In' link in header")
    def click_sign_in_link(self) -> SignInModal:
        """ Click on the Sign In link in the header. """
        self.click(self.sign_in_locator)
        return SignInModal(self.get_driver())

    @allure.step("Click 'My Space' link in header")
    def click_my_space_link(self) -> "MySpaceHabitsTabPage":
        """ Click on the My Space link in the header. """
        self.click(self.my_space_link_locator)
        from pages.my_space.my_space_habits_tab_page import MySpaceHabitsTabPage
        return MySpaceHabitsTabPage(self.get_driver())

    @allure.step("Click 'Sign Up' link in header")
    def click_sign_up_link(self) -> SignUpModal:
        """Click on the Sign Up link in the header."""
        self.click(self.sign_up_locator)
        return SignUpModal(self.get_driver())

    @allure.step("Click search button in header")
    def click_search_btn(self):
        """Click on the search button in the header."""
        self.click(self.search_btn_locator)

    @allure.step("Open language dropdown")
    def click_language_dropdown(self):
        """Click on the language dropdown button."""
        self.click(self.language_dropdown_locator)

    @allure.step("Get current locale")
    def get_current_locale(self) -> Language:
        """Get the currently selected language, returns 'uk' or 'en'."""
        lang = self.find(*self.language_dropdown_locator).text.strip()
        return Language.UK if lang.lower() == "uk" else Language.EN

    def _language_option_locator(self, lang: Language) -> Tuple[str, str]:
        """ Generate locator for a language option inside the language dropdown. """
        return By.XPATH, f"//span[text()='{lang.value}']"

    def _switch_language(self, lang: Language):
        """Switch to the specified language if not already selected."""
        if self.get_current_locale() == lang.locale_code:
            return self
        self.click(self.language_dropdown_locator)
        self.click(self._language_option_locator(lang))
        return self

    @allure.step("Change language to English")
    def change_to_en(self) -> HeaderComponent:
        """Switch header language to English."""
        return self._switch_language(Language.EN)

    @allure.step("Change language to Ukrainian")
    def change_to_uk(self) -> HeaderComponent:
        """Switch header language to Ukrainian."""
        return self._switch_language(Language.UK)

    @allure.step("Get logged-in user name")
    def get_user(self) -> str:
        """Get the name of the logged-in user, return empty string if not present."""
        try:
            user_elem = self.wait_until_visible(*self.user_name_locator)
            return user_elem.text.strip()
        except Exception:
            return ""

    @allure.step("Open profile dropdown")
    def click_profile_dropdown(self) -> "ProfileDropdownComponent":
        """Click the profile dropdown button and return the ProfileDropdownComponent."""
        self.click(self.user_name_locator)
        dropdown = self.wait_until_visible(*self.user_dropdown_locator)
        from components.profile_dropdown_component import ProfileDropdownComponent
        return ProfileDropdownComponent(self.get_driver(), dropdown)
