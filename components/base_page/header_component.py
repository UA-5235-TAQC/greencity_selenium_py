from __future__ import annotations

from typing import Tuple, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from components.auth_modal.sign_in_modal import SignInModal
from components.auth_modal.sign_up_modal import SignUpModal
from components.base_component import BaseComponent
import allure

from enums.language import Language
from utils.page_factory import LocatorsTable

from components.base_page.profile_dropdown_component import ProfileDropdownComponent


class HeaderComponent(BaseComponent):
    """ Represents the header section of the GreenCity application. """

    logo: WebElement
    news_link: WebElement
    my_space_link: WebElement
    sign_in: WebElement
    sign_up: WebElement
    search_btn: WebElement
    language_dropdown: WebElement
    user_name: WebElement
    user_dropdown: ProfileDropdownComponent

    auth_modal_sign_in: SignInModal
    auth_modal_sign_up: SignUpModal

    locators: LocatorsTable = {
        "logo": (By.CSS_SELECTOR, 'a.header_logo'),
        "news_link": (By.XPATH, "//a[contains(@href, '#/greenCity/news')]"),
        "my_space_link": (By.XPATH, "//a[contains(@href, '#/greenCity/profile')]"),
        "sign_in": (By.CSS_SELECTOR, "a.header_sign-in-link"),
        "sign_up": (By.CSS_SELECTOR, "li.header_sign-up-link"),
        "search_btn": (By.CSS_SELECTOR, "li.search-icon"),
        "language_dropdown": (By.CSS_SELECTOR, "ul.header_lang-switcher-wrp"),
        "user_name": (By.CSS_SELECTOR, ".body-2"),
        "user_dropdown": (By.CSS_SELECTOR, "ul.dropdown-list", ProfileDropdownComponent),
        "auth_modal_sign_in": (By.XPATH, "//app-auth-modal", SignInModal),
        "auth_modal_sign_up": (By.XPATH, "//app-auth-modal", SignUpModal)
    }

    @allure.step("Click header logo")
    def click_logo(self) -> "HomePage":
        """ Click on the logo in the header to navigate to the home page. """
        self.logo.click()
        from pages.home_page import HomePage
        return HomePage(self.driver)

    @allure.step("Click 'Eco News' link in header")
    def click_news_link(self) -> "NewsPage":
        """ Click on the news link in the header to navigate to the Eco News page. """
        self.news_link.click()
        from pages.news_page import NewsPage
        return NewsPage(self.driver).wait_until_opened()

    @allure.step("Click 'Sign In' link in header")
    def click_sign_in_link(self) -> SignInModal:
        """ Click on the Sign In link in the header. """
        self.sign_in.click()
        return self.auth_modal_sign_in

    @allure.step("Click 'My Space' link in header")
    def click_my_space_link(self) -> "MySpaceHabitsTabPage":
        """ Click on the My Space link in the header. """
        self.my_space_link.click()
        from pages.my_space.my_space_habits_tab_page import MySpaceHabitsTabPage
        return MySpaceHabitsTabPage(self.driver)

    @allure.step("Click 'Sign Up' link in header")
    def click_sign_up_link(self) -> SignUpModal:
        """Click on the Sign Up link and return SignUpModal."""
        self.sign_up.click()
        return self.auth_modal_sign_up

    @allure.step("Click search button in header")
    def click_search_btn(self):
        """Click on the search button in the header."""
        self.search_btn.click()

    @allure.step("Open language dropdown")
    def click_language_dropdown(self):
        """Click on the language dropdown button."""
        self.language_dropdown.click()

    @allure.step("Get current locale")
    def get_current_locale(self) -> Language:
        """Get the currently selected language, returns 'uk' or 'en'."""
        lang = self.language_dropdown.text.strip()
        return Language.UK if lang.lower() == "uk" else Language.EN

    def _language_option_locator(self, lang: Language) -> Tuple[str, str]:
        """ Generate locator for a language option inside the language dropdown. """
        return By.XPATH, f"//span[text()='{lang.value}']"

    def _switch_language(self, lang: Language):
        """ Switch the header language to the specified language. """
        if self.get_current_locale() == lang:
            return self
        self.language_dropdown.click()
        self.driver.find_element(*self._language_option_locator(lang)).click()
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
        return self.user_name.text.strip()

    @allure.step("Open profile dropdown")
    def click_profile_dropdown(self) -> ProfileDropdownComponent:
        """Click the profile dropdown button and return the ProfileDropdownComponent."""
        self.user_name.click()
        dropdown = self.user_dropdown
        return ProfileDropdownComponent(dropdown)
