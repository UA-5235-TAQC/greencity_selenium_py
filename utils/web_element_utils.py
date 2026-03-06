from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


def get_int_from_text(element: WebElement, part_index: int = None) -> int:
    """ Get an integer value from the text of the element. """
    text = element.text

    if part_index is not None:
        parts = text.split()
        text = parts[part_index] if part_index < len(parts) else ""

    digits = "".join(c for c in text if c.isdigit())
    return int(digits) if digits else 0


def clear_element_by_keyboard(element: WebElement):
    """ Clear input element using keyboard shortcuts. """
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)


def enter_text(element: WebElement, text: str):
    """Generic helper to clear an input field and type text into it."""
    element.click()
    clear_element_by_keyboard(element)
    element.send_keys(text)
