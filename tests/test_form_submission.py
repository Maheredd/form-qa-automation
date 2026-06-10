import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import BASE_URL as FORM_URL


# -------------------------------------------------------
# Fixtures
# -------------------------------------------------------

@pytest.fixture(scope="module")
def driver():
    """Launch Chrome and open the form page."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    driver.get(FORM_URL)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def scroll_to(driver, element):
    """Scroll element into view."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)


def scroll_and_click(driver, element):
    """Scroll into view and click."""
    scroll_to(driver, element)
    element.click()


def wait_for(driver, by, value, timeout=10):
    """Wait for an element to be present and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_clickable(driver, by, value, timeout=10):
    """Wait for an element to be clickable and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


# -------------------------------------------------------
# Test Data
# -------------------------------------------------------

VALID_FORM_DATA = {
    "first_name": "Mahesh",
    "last_name": "G",
    "email": "mahesh@example.com",
    "phone": "9110815046",
    "gender": "Male",
    "dob": "10 May 2001",
    "subject": "Computer Science",
    "hobby": "Sports",
    "address": "123 MG Road, Bengaluru, Karnataka",
    "state": "NCR",
    "city": "Delhi",
}


# -------------------------------------------------------
# Test Cases
# -------------------------------------------------------

@allure.feature("Form Submission")
@allure.story("Successful End-to-End Submission")
@allure.severity(allure.severity_level.CRITICAL)
def test_full_form_submission(driver):
    """
    TC-013: Fill all required fields with valid data and submit.
    Verify the confirmation modal appears with correct details.
    """

    # --- Step 1: Fill First Name ---
    with allure.step("Enter First Name"):
        first_name = wait_for(driver, By.ID, "firstName")
        first_name.clear()
        first_name.send_keys(VALID_FORM_DATA["first_name"])

    # --- Step 2: Fill Last Name ---
    with allure.step("Enter Last Name"):
        last_name = wait_for(driver, By.ID, "lastName")
        last_name.clear()
        last_name.send_keys(VALID_FORM_DATA["last_name"])

    # --- Step 3: Fill Email ---
    with allure.step("Enter Email"):
        email = wait_for(driver, By.ID, "userEmail")
        email.clear()
        email.send_keys(VALID_FORM_DATA["email"])

    # --- Step 4: Select Gender ---
    with allure.step("Select Gender"):
        gender_label = driver.find_element(
            By.XPATH, f"//label[text()='{VALID_FORM_DATA['gender']}']"
        )
        scroll_and_click(driver, gender_label)

    # --- Step 5: Fill Phone Number ---
    with allure.step("Enter Phone Number"):
        phone = wait_for(driver, By.ID, "userNumber")
        phone.clear()
        phone.send_keys(VALID_FORM_DATA["phone"])

    # --- Step 6: Set Date of Birth ---
    with allure.step("Set Date of Birth"):
        dob_field = wait_for(driver, By.ID, "dateOfBirthInput")
        scroll_and_click(driver, dob_field)
        dob_field.clear()
        dob_field.send_keys(VALID_FORM_DATA["dob"])

    # --- Step 7: Enter Subject ---
    with allure.step("Enter Subject"):
        subject_input = wait_for(driver, By.ID, "subjectsInput")
        scroll_to(driver, subject_input)
        subject_input.send_keys(VALID_FORM_DATA["subject"])
        # Wait for autocomplete suggestion and click it
        suggestion = wait_for_clickable(
            driver, By.XPATH,
            f"//div[contains(@class,'subjects-auto-complete__option') and contains(text(),'{VALID_FORM_DATA['subject']}')]"
        )
        suggestion.click()

    # --- Step 8: Select Hobby ---
    with allure.step("Select Hobby"):
        hobby_label = driver.find_element(
            By.XPATH, f"//label[text()='{VALID_FORM_DATA['hobby']}']"
        )
        scroll_and_click(driver, hobby_label)

    # --- Step 9: Enter Current Address ---
    with allure.step("Enter Current Address"):
        address = wait_for(driver, By.ID, "currentAddress")
        scroll_to(driver, address)
        address.clear()
        address.send_keys(VALID_FORM_DATA["address"])

    # --- Step 10: Select State ---
    with allure.step("Select State"):
        state_dropdown = wait_for_clickable(driver, By.ID, "react-select-3-input")
        scroll_to(driver, state_dropdown)
        state_dropdown.send_keys(VALID_FORM_DATA["state"])
        state_option = wait_for_clickable(
            driver, By.XPATH,
            f"//div[contains(@class,'option') and text()='{VALID_FORM_DATA['state']}']"
        )
        state_option.click()

    # --- Step 11: Select City ---
    with allure.step("Select City"):
        city_dropdown = wait_for_clickable(driver, By.ID, "react-select-4-input")
        city_dropdown.send_keys(VALID_FORM_DATA["city"])
        city_option = wait_for_clickable(
            driver, By.XPATH,
            f"//div[contains(@class,'option') and text()='{VALID_FORM_DATA['city']}']"
        )
        city_option.click()

    # --- Step 12: Submit the Form ---
    with allure.step("Click Submit Button"):
        submit_btn = wait_for_clickable(driver, By.ID, "submit")
        scroll_and_click(driver, submit_btn)

    # --- Step 13: Verify Confirmation Modal ---
    with allure.step("Verify Confirmation Modal Appears"):
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        assert modal.is_displayed(), \
            "BUG: Confirmation modal did not appear after valid form submission!"
        assert "Thanks for submitting the form" in modal.text, \
            "BUG: Confirmation modal title text is incorrect!"

    # --- Step 14: Verify Submitted Data in Modal ---
    with allure.step("Verify Submitted Data in Modal"):
        modal_body = driver.find_element(By.CLASS_NAME, "table-responsive")
        modal_text = modal_body.text

        assert VALID_FORM_DATA["first_name"] in modal_text, \
            "BUG: First name not found in confirmation modal!"
        assert VALID_FORM_DATA["email"] in modal_text, \
            "BUG: Email not found in confirmation modal!"
        assert VALID_FORM_DATA["phone"] in modal_text, \
            "BUG: Phone number not found in confirmation modal!"

    # Attach modal screenshot to Allure report
    allure.attach(
        driver.get_screenshot_as_png(),
        name="Confirmation Modal",
        attachment_type=allure.attachment_type.PNG
    )


@allure.feature("Form Submission")
@allure.story("Submit With Only Required Fields")
@allure.severity(allure.severity_level.NORMAL)
def test_submit_with_only_required_fields(driver):
    """
    TC-014: Fill only mandatory fields (name, gender, phone)
    and submit. Form should still succeed.
    """
    driver.get(FORM_URL)

    with allure.step("Enter First Name"):
        first_name = wait_for(driver, By.ID, "firstName")
        first_name.send_keys("Mahesh")

    with allure.step("Enter Last Name"):
        last_name = wait_for(driver, By.ID, "lastName")
        last_name.send_keys("G")

    with allure.step("Select Gender"):
        gender_label = driver.find_element(By.XPATH, "//label[text()='Male']")
        scroll_and_click(driver, gender_label)

    with allure.step("Enter Phone Number"):
        phone = wait_for(driver, By.ID, "userNumber")
        phone.send_keys("9110815046")

    with allure.step("Submit Form"):
        submit_btn = wait_for_clickable(driver, By.ID, "submit")
        scroll_and_click(driver, submit_btn)

    with allure.step("Verify Modal Appears"):
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        assert modal.is_displayed(), \
            "BUG: Form with only required fields did not submit successfully!"


@allure.feature("Form Submission")
@allure.story("Close Confirmation Modal")
@allure.severity(allure.severity_level.NORMAL)
def test_close_confirmation_modal(driver):
    """
    TC-015: After successful submission, clicking Close
    should dismiss the modal and return to the form.
    """
    with allure.step("Click Close Button on Modal"):
        close_btn = wait_for_clickable(driver, By.ID, "closeLargeModal")
        close_btn.click()

    with allure.step("Verify Modal is Dismissed"):
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        assert "index.html" in driver.current_url, \
            "BUG: Page navigated away after closing the modal!"
