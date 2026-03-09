import allure
from allure_commons.types import Severity
from selenium.common.exceptions import StaleElementReferenceException
from pages.home_page import HomePage

@allure.tag("Auth")
@allure.epic("Authentication")
@allure.feature("Sign Up")
@allure.story("Verify Sign Up modal functionality")
@allure.severity(Severity.CRITICAL)
class TestSignUpModal:
    """Tests for the Sign Up modal window."""
    
    @allure.title("Sign Up modal opens after clicking 'Sign Up' in header")
    @allure.description("Verify that clicking 'Sign Up' in the header opens the Sign Up modal")
    def test_sign_up_modal_opens(self, get_driver):
        """Verify Sign Up modal opens and displays the correct title."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.wait_for(lambda _: sign_up_modal.get_title() == "Hello!")
        assert sign_up_modal.get_title() == "Hello!", "Sign Up modal title should be 'Hello!'"

    @allure.title("Sign Up submit button is disabled by default")
    @allure.description("Verify that the submit button is disabled when the form is empty")
    def test_sign_up_submit_button_disabled(self, get_driver):
        """Verify that the Sign Up button cannot be clicked without filling the form."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.wait_for(lambda _: sign_up_modal.get_title() == "Hello!")
        assert not sign_up_modal.is_submit_button_enabled(), "Sign Up submit button should be disabled when fields are empty"

    @allure.title("Password mismatch shows error in Sign Up modal")
    @allure.description("Verify that entering non-matching passwords triggers a confirm password error")
    def test_sign_up_password_mismatch_error(self, get_driver):
        """Verify that mismatching passwords trigger a confirm password validation error."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.enter_password("Password1!")
        sign_up_modal.enter_confirm_password("DifferentPassword1!")
        sign_up_modal.email_field.click()
        sign_up_modal.wait_for(lambda _: sign_up_modal.is_invalid_confirm_password_error_displayed())
        assert sign_up_modal.is_invalid_confirm_password_error_displayed(), "Confirm password error should be shown when passwords do not match"

    @allure.title("Invalid email shows error in Sign Up modal")
    @allure.description("Verify that an invalid email format triggers an email validation error")
    def test_sign_up_invalid_email_error(self, get_driver):
        """Verify that an invalid email triggers a validation error."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.enter_email("invalid-email")
        sign_up_modal.username_field.click()
        sign_up_modal.wait_for(lambda _: sign_up_modal.is_invalid_email_error_displayed())
        assert sign_up_modal.is_invalid_email_error_displayed(), "Email validation error should be displayed for invalid email in Sign Up modal"

    @allure.title("Clicking 'Sign In' link in Sign Up modal opens Sign In modal")
    @allure.description("Verify that the Sign In link inside Sign Up modal navigates back to Sign In form")
    def test_sign_up_navigate_to_sign_in(self, get_driver):
        """Verify Sign In link inside Sign Up modal opens the Sign In modal."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        get_driver.execute_script("arguments[0].click();", sign_up_modal.sign_in_link)
        sign_in_modal = home_page.header.auth_modal_sign_in
        sign_in_modal.wait_for(lambda _: sign_in_modal.get_title() == "Welcome back!")
        assert sign_in_modal.get_title() == "Welcome back!", "Sign In modal title should be 'Welcome back!' after clicking Sign In link"

    @allure.title("Sign Up modal closes after clicking the close button")
    @allure.description("Verify that clicking the close button hides the Sign Up modal")
    def test_sign_up_modal_closes(self, get_driver):
        """Verify that the close button dismisses the Sign Up modal."""
        get_driver.maximize_window()
        home_page = HomePage(get_driver).open()
        get_driver.execute_script("arguments[0].click();", home_page.header.sign_up)
        sign_up_modal = home_page.header.auth_modal_sign_up
        sign_up_modal.close_modal()
        sign_up_modal.wait_until_closed()
        try:
            is_displayed = sign_up_modal.is_visible()
        except StaleElementReferenceException:
            is_displayed = False
        assert not is_displayed, "Sign Up modal should not be visible after clicking close"