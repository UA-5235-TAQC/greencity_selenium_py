from __future__ import annotations
from selenium.webdriver.common.by import By
from components.auth_modal.sign_up_modal import SignUpModal
from components.profile_dropdown_component import ProfileDropdownComponent
from components.base_component import BaseComponent
from selenium.webdriver.support import expected_conditions as EC


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

    def click_logo(self) -> "HomePage":
        """ Click on the logo in the header to navigate to the home page. """
        self._click(self.logo_locator)
        from pages.home_page import HomePage
        return HomePage(self.get_driver())

    def wait_until_url_contains(self, value: str):
        """Wait until current URL contains given value."""
        self.wait.until(EC.url_contains(value))

    def click_news_link(self) -> "NewsPage":
        """ Click on the news link in the header to navigate to the Eco News page. """
        self._click(self.news_link_locator)
        self.wait_until_url_contains("/news")
        from pages.news_page import NewsPage
        return NewsPage(self.get_driver())

    def click_sign_in_link(self):
        """ Click on the sign-in link in the header. """
        self._click(self.sign_in_locator)

    def click_my_space_link(self):
        """ Click on the My Space link in the header. """
        self._click(self.my_space_link_locator)

    def _click(self, locator: tuple):
        """ Find an element by locator within the header root and click it. """
        element = self.get_driver().find_element(*locator)
        self.wait_until_clickable(locator)
        element.click()

    def click_sign_up_link(self) -> SignUpModal:
        """Click on the Sign Up link in the header."""
        self.get_driver().find_element(*self.sign_up_locator).click()
        return SignUpModal(self.get_driver())

    def click_search_btn(self):
        """Click on the search button in the header."""
        self.get_driver().find_element(*self.search_btn_locator).click()

    def click_language_dropdown(self):
        """Click on the language dropdown button."""
        self.get_driver().find_element(*self.language_dropdown_locator).click()

    def change_to_en(self) -> HeaderComponent:
        """Switch header language to English."""
        return self._switch_language("En")

    def change_to_uk(self) -> HeaderComponent:
        """Switch header language to Ukrainian."""
        return self._switch_language("Uk")

    def _switch_language(self, lang: str) -> HeaderComponent:
        """Switch to the specified language if not already selected."""
        dropdown = self.get_driver().find_element(*self.language_dropdown_locator)
        current_lang = dropdown.text.strip()
        if current_lang.lower() == lang.lower():
            return self
        dropdown.click()
        option = dropdown.find_element(By.XPATH, f".//span[text()='{lang}']")
        self.wait_until_clickable(option)
        option.click()
        return self

    def get_user(self) -> str:
        """Get the name of the logged-in user, return empty string if not present."""
        try:
            user_elem = self.get_driver().find_element(*self.user_name_locator)
            self.wait_until_visible(user_elem)
            return user_elem.text.strip()
        except Exception:
            return ""

    def click_profile_dropdown(self) -> ProfileDropdownComponent:
        """Click the profile dropdown button and return the ProfileDropdownComponent."""
        drp_button = self.get_driver().find_element(*self.user_name_locator)
        self.wait_until_clickable(drp_button)
        drp_button.click()
        dropdown = self.get_driver().find_element(*self.user_dropdown_locator)
        self.wait_until_visible(dropdown)
        return ProfileDropdownComponent(self.get_driver(), dropdown)

    def get_current_locale(self) -> str:
        """Get the currently selected language, returns 'uk' or 'en'."""
        lang = self.get_driver().find_element(*self.language_dropdown_locator).text.strip()
        return "uk" if lang.lower() == "uk" else "en"
