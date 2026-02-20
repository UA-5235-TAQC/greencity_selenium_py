from __future__ import annotations

from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class HeaderComponent(BaseComponent):
    logo_locator = (By.CSS_SELECTOR, 'a.header_logo')
    news_link_locator = (By.XPATH, "//a[contains(@href, '#/greenCity/news')]")
    my_space_link_locator = (By.XPATH, "//a[contains(@href, '#/greenCity/profile')]")
    sign_in_locator = (By.CSS_SELECTOR, "a.header_sign-in-link")

    def click_logo(self) -> "HomePage":
        logo = self.root.find_element(*self.logo_locator)
        logo.click()
        from pages.home_page import HomePage
        return HomePage(self.get_driver())

    def click_news_link(self) -> "NewsPage":
        news_link = self.root.find_element(*self.news_link_locator)
        news_link.click()
        from pages.news_page import NewsPage
        return NewsPage(self.get_driver())

    def click_sign_in_link(self):
        sign_in_link = self.root.find_element(*self.sign_in_locator)
        sign_in_link.click()

    def click_my_space_link(self):
        my_space_link = self.root.find_element(*self.my_space_link_locator)
        my_space_link.click()
