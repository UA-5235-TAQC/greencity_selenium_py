import allure
from allure_commons.types import Severity
from selenium.common.exceptions import StaleElementReferenceException
from pages.home_page import HomePage

@allure.tag("Auth")
@allure.epic("Authentication")
@allure.feature("Sign In")
@allure.story("Verify Sign In modal functionality")
@allure.severity(Severity.CRITICAL)
class TestSignInModal:
    """Tests for the Sign In modal window."""
    @allure.title("Sign In modal opens after clicking 'Sign In' in header")
    @allure.description("Verify that clicking 'Sign In' in the header opens the auth modal with correct title")
    def test_sign_in_modal_opens(self, get_driver):
        """Verify Sign In modal opens and displays the correct title."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_in)
        sign_in_modal = home_page.header.auth_modal_sign_in
        sign_in_modal.wait_for(lambda _: sign_in_modal.get_title() == "Welcome back!")
        assert sign_in_modal.get_title() == "Welcome back!", \
            "Sign In modal title should be 'Welcome back!'"

    @allure.title("Invalid email shows validation error in Sign In modal")
    @allure.description("Verify that entering an invalid email triggers an email validation error")
    def test_sign_in_invalid_email_shows_error(self, get_driver):
        """Verify that an invalid email format triggers an error message."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_in)
        sign_in_modal = home_page.header.auth_modal_sign_in
        sign_in_modal.enter_email("not-an-email")
        sign_in_modal.email_field.send_keys("\t")
        sign_in_modal.wait_for(lambda _: sign_in_modal.is_invalid_email_error_displayed())
        assert sign_in_modal.is_invalid_email_error_displayed(), \
            "Email validation error should be displayed for invalid email"

    @allure.title("Empty password shows validation error in Sign In modal")
    @allure.description("Verify that submitting the form with empty password shows password error")
    def test_sign_in_empty_password_shows_error(self, get_driver):
        """Verify that submitting without a password shows a password validation error."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_in)
        sign_in_modal = home_page.header.auth_modal_sign_in
        sign_in_modal.enter_email("test@test.com")
        sign_in_modal.password_field.click()
        sign_in_modal.password_field.send_keys("\t")
        sign_in_modal.click_submit()
        sign_in_modal.wait_for(lambda _: sign_in_modal.is_invalid_password_error_displayed())
        assert sign_in_modal.is_invalid_password_error_displayed(), \
            "Password validation error should be shown when password is empty"

    @allure.title("Clicking 'Sign Up' link in Sign In modal opens Sign Up modal")
    @allure.description("Verify that the Sign Up link inside Sign In modal navigates to Sign Up form")
    def test_sign_in_navigate_to_sign_up(self, get_driver):
        """Verify Sign Up link inside Sign In modal opens the Sign Up modal."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_in)
        sign_in_modal = home_page.header.auth_modal_sign_in
        get_driver.execute_script("arguments[0].click();", sign_in_modal.sign_up_link)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.wait_for(lambda _: sign_up_modal.get_title() == "Hello!")
        assert sign_up_modal.get_title() == "Hello!", \
            "Sign Up modal title should be 'Hello!' after clicking Sign Up link"

    @allure.title("Sign In modal closes after clicking the close button")
    @allure.description("Verify that clicking the close button hides the Sign In modal")
    def test_sign_in_modal_closes(self, get_driver):
        """Verify that the close button dismisses the Sign In modal."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_in)
        sign_in_modal = home_page.header.auth_modal_sign_in
        sign_in_modal.close_modal()
        sign_in_modal.wait_until_closed()
        try:
            is_displayed = sign_in_modal.is_visible()
        except StaleElementReferenceException:
            is_displayed = False
        assert not is_displayed, "Sign In modal should not be visible after clicking close"