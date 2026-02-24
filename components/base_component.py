import allure

from utils.page_factory import PageFactory


class BaseComponent(PageFactory):
    """ Base class for page components. """

    @allure.step("Check if the component is enabled")
    def is_enabled(self) -> bool:
        """Check if the component is enabled."""
        return self.root_element.is_enabled()

    @allure.step("Check if the component is visible")
    def is_component_visible(self) -> bool:
        """Check if the component is visible."""
        return self.root_element.is_displayed()
