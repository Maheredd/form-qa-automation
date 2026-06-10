import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

# URL of the demo form
FORM_URL = "https://demoqa.com/automation-practice-form"


@pytest.fixture(scope="module")
def driver():
    """Setup Chrome browser and open the form page."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(FORM_URL)
    yield driver
    driver.quit()


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def scroll_and_click(driver, element):
    """Scroll element into view then click it."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Use JS click to bypass the overlapping footer ad on demoqa.com
    driver.execute_script("arguments[0].click();", element)


def get_field(driver, field_id):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, field_id))
    )


# -------------------------------------------------------
# Test Cases
# -------------------------------------------------------

@allure.feature("Field Validation")
@allure.story("Empty Required Fields")
@allure.severity(allure.severity_level.CRITICAL)
def test_submit_empty_form(driver):
    """
    TC-001: Submitting the form without filling any field
    should NOT navigate away or show a success message.
    """
    submit_btn = driver.find_element(By.ID, "submit")
    scroll_and_click(driver, submit_btn)

    # Page should still be on the same URL
    assert "automation-practice-form" in driver.current_url, \
        "BUG: Form submitted successfully with all fields empty!"


@allure.feature("Field Validation")
@allure.story("Invalid Email Format")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("invalid_email", [
    "plaintext",
    "missing@domain",
    "@nodomain.com",
    "spaces in@email.com",
    "double@@email.com",
])
def test_invalid_email_formats(driver, invalid_email):
    """
    TC-002: Email field should reject invalid formats.
    """
    email_field = get_field(driver, "userEmail")
    email_field.clear()
    email_field.send_keys(invalid_email)

    submit_btn = driver.find_element(By.ID, "submit")
    scroll_and_click(driver, submit_btn)

    # Check field border turns red (invalid state)
    border_color = email_field.value_of_css_property("border-color")
    assert "rgb(220, 53, 69)" in border_color or "rgb(215, 55, 69)" in border_color, \
        f"BUG: Invalid email '{invalid_email}' was accepted without an error!"


@allure.feature("Field Validation")
@allure.story("Valid Email Format")
@allure.severity(allure.severity_level.NORMAL)
def test_valid_email_accepted(driver):
    """
    TC-003: A valid email should be accepted without errors.
    """
    email_field = get_field(driver, "userEmail")
    email_field.clear()
    email_field.send_keys("mahesh@example.com")

    # Field border should NOT be red
    border_color = email_field.value_of_css_property("border-color")
    assert "rgb(220, 53, 69)" not in border_color and "rgb(215, 55, 69)" not in border_color, \
        "BUG: Valid email flagged as invalid!"


@allure.feature("Field Validation")
@allure.story("First Name - Empty")
@allure.severity(allure.severity_level.CRITICAL)
def test_empty_first_name(driver):
    """
    TC-004: First name field should not accept empty submission.
    """
    first_name = get_field(driver, "firstName")
    first_name.clear()

    submit_btn = driver.find_element(By.ID, "submit")
    scroll_and_click(driver, submit_btn)

    border_color = first_name.value_of_css_property("border-color")
    assert "rgb(220, 53, 69)" in border_color or "rgb(215, 55, 69)" in border_color, \
        "BUG: Form accepted empty first name!"


@allure.feature("Field Validation")
@allure.story("First Name - Special Characters")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("special_input", [
    "123456",
    "!@#$%^",
    "<script>alert('xss')</script>",
])
def test_first_name_special_characters(driver, special_input):
    """
    TC-005: First name should ideally not accept numbers or special characters.
    Log as observation if accepted (may be a bug depending on requirements).
    """
    first_name = get_field(driver, "firstName")
    first_name.clear()
    first_name.send_keys(special_input)

    value = first_name.get_attribute("value")
    # Log observation — mark as warning, not hard fail
    print(f"[OBSERVATION] First name accepted: '{value}' — verify with requirements.")


@allure.feature("Field Validation")
@allure.story("Phone Number - Invalid Format")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("invalid_phone", [
    "123",           # too short
    "abcdefghij",    # letters
    "12345678901234"  # too long
])
def test_invalid_phone_number(driver, invalid_phone):
    """
    TC-006: Mobile number field should only accept valid 10-digit numbers.
    """
    phone_field = get_field(driver, "userNumber")
    phone_field.clear()
    phone_field.send_keys(invalid_phone)

    submit_btn = driver.find_element(By.ID, "submit")
    scroll_and_click(driver, submit_btn)

    border_color = phone_field.value_of_css_property("border-color")
    assert "rgb(220, 53, 69)" in border_color or "rgb(215, 55, 69)" in border_color, \
        f"BUG: Invalid phone '{invalid_phone}' was accepted!"


@allure.feature("Field Validation")
@allure.story("Phone Number - Valid")
@allure.severity(allure.severity_level.NORMAL)
def test_valid_phone_number(driver):
    """
    TC-007: A valid 10-digit phone number should be accepted.
    """
    phone_field = get_field(driver, "userNumber")
    phone_field.clear()
    phone_field.send_keys("9110815046")

    border_color = phone_field.value_of_css_property("border-color")
    assert "rgb(220, 53, 69)" not in border_color and "rgb(215, 55, 69)" not in border_color, \
        "BUG: Valid phone number flagged as invalid!"
