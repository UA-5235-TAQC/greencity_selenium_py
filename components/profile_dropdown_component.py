import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from components.base_component import BaseComponent


class ProfileDropdownComponent(BaseComponent):
    _links = (By.CSS_SELECTOR, "a")

    def __init__(self, root, driver, timeout=None):
        super().__init__(root, driver, timeout)

    def _get_links(self):
        self.wait.until(EC.visibility_of_any_elements_located(self._links))
        return self.root.find_elements(*self._links)

    @allure.step("Open notifications")
    def open_notifications(self):
        links = self._get_links()
        if links:
            links[0].click()

    @allure.step("Open personal account page")
    def open_personal_account(self):
        links = self._get_links()
        if len(links) > 1:
            links[1].click()

    @allure.step("Click Sign Out")
    def sign_out(self):
        links = self._get_links()
        if links:
            links[-1].click()
