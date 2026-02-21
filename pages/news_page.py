from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support import expected_conditions as EC


class NewsPage(BasePage):
    """ Page Object representing the Eco News page. """

    page_title_locator = (By.CSS_SELECTOR, "h1.main-header")
    create_news_btn_locator = (By.CSS_SELECTOR, "div#create-button")
    tags_locator = (By.CSS_SELECTOR, "[aria-label='filter by items']")
    remaining_count_text_locator = (By.CSS_SELECTOR, "h2")
    cards_locator = (By.CSS_SELECTOR, "ul.list")

    grid_view_btn_locator = (By.CSS_SELECTOR, "[aria-label='table view']")
    list_view_btn_locator = (By.CSS_SELECTOR, "[aria-label='list view']")

    my_events_btn_locator = (By.CSS_SELECTOR, "div:has(img.my-events-img)")
    bookmark_btn_locator = (By.CSS_SELECTOR, "div:has(span.bookmark-img)")
    search_btn_locator = (By.CSS_SELECTOR, "div:has(span.search-img)")

    search_input_locator = (By.CSS_SELECTOR, "input.place-input")
    close_search_icon_locator = (By.CSS_SELECTOR, "img[alt='cancel search']")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Open Eco News page")
    def open(self):
        """ Navigate to the Eco News page. """
        self.driver.get(self.get_base_host() + "/news")
        return self

    @allure.step("Verify Eco News page is opened")
    def is_page_opened(self):
        """ Check whether the Eco News page is opened. """
        return self.is_visible(*self.page_title_locator)

    @allure.step("Wait until Eco News page is opened")
    def wait_until_opened(self):
        """ Wait until the Eco News page title becomes visible. """
        self.wait.until(EC.visibility_of_element_located(self.page_title_locator))
        return self

    @allure.step("Get Eco News page title")
    def get_page_title(self) -> str:
        """ Retrieve the text of the Eco News page title. """
        return self.driver.find_element(*self.page_title_locator).text

    @allure.step("Enter search text: {text}")
    def enter_search(self, text: str):
        """
        Enter text into the search input field.
        If the search input is not visible, the search button is clicked first.
        """
        search_input = self.driver.find_element(*self.search_input_locator)
        if not search_input.is_displayed():
            self.driver.find_element(*self.search_btn_locator).click()
        search_input.send_keys(text)

    @allure.step("Close search input")
    def close_search(self):
        """ Close the search input field if it is currently visible. """
        search_input = self.driver.find_element(*self.search_input_locator)
        if search_input.is_displayed():
            self.driver.find_element(*self.close_search_icon_locator).click()

    @allure.step("Click Bookmark button")
    def click_bookmark(self):
        """ Click the Bookmark filter button. """
        self.driver.find_element(*self.bookmark_btn_locator).click()

    @allure.step("Click My Events button")
    def click_my_events(self):
        """ Click the My Events filter button. """
        self.driver.find_element(*self.my_events_btn_locator).click()

    @allure.step("Switch news list view to grid")
    def switch_to_grid_view(self):
        """ Switch the news list display to grid view. """
        self.driver.find_element(*self.grid_view_btn_locator).click()

    @allure.step("Switch news list view to list")
    def switch_to_list_view(self):
        """ Switch the news list display to list view. """
        self.driver.find_element(*self.list_view_btn_locator).click()
