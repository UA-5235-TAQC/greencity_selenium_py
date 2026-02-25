import allure

from components.base_component import BaseComponent


class TagItem(BaseComponent):
    """Represents a tag item component on the EcoNews page."""

    NAME = ("css selector", "a.global-tag .text")
    CLOSE_ICON = ("css selector", "a.global-tag div")

    @allure.step("Get tag name")
    def get_name(self) -> str:
        """ Return the visible text of the tag. """
        return self.get_text(self.NAME)

    @allure.step("Verify if tag is selected")
    def is_selected(self) -> bool:
        """ Check if the tag is selected. """
        classes = self.find(self.CLOSE_ICON).get_attribute("class")
        return classes is not None and "global-tag-close-icon" in classes

    @allure.step("Click on tag")
    def click_tag(self):
        """ Click on the tag's name element. """
        self.click(self.NAME)
