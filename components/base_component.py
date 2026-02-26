import allure

from utils.page_factory import PageFactory


class BaseComponent(PageFactory):
    """ Base class for page components. """

    def __init__(self, driver):
        """ Initialize the base component with a WebDriver instance and merge all declared locators. """
        all_locators = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'locators'):
                all_locators.update(cls.locators)

        self.locators = all_locators
        super().__init__(driver)

    @allure.step("Check if the component is enabled")
    def is_enabled(self) -> bool:
        """Check if the component is enabled."""
        return self.root_element.is_enabled()

    @allure.step("Check if the component is visible")
    def is_component_visible(self) -> bool:
        """Check if the component is visible."""
        return self.root_element.is_displayed()
