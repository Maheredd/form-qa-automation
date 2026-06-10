import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the demo form
FORM_URL = "https://demoqa.com/automation-practice-form"

# -------------------------------------------------------
# Helper: Create temporary test files
# -------------------------------------------------------


def create_temp_file(filename, size_kb=10):
    """
    Creates a temporary file in the current directory.
    size_kb controls the file size (default 10KB).
    Returns the absolute path of the created file.
    """
    filepath = os.path.abspath(filename)
    with open(filepath, "wb") as f:
        f.write(b"A" * size_kb * 1024)  # fill with dummy bytes
    return filepath


def create_pdf_file(filename):
    """
    Creates a minimal valid-looking PDF file for upload testing.
    Returns the absolute path.
    """
    filepath = os.path.abspath(filename)
    with open(filepath, "wb") as f:
        # Minimal PDF header so the OS recognizes it as PDF
        f.write(b"%PDF-1.4\n%Fake resume content for testing\n")
    return filepath


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


@pytest.fixture(scope="module", autouse=True)
def temp_files():
    """
    Create all temp test files before the module runs,
    and clean them up after all tests finish.
    """
    files = [
        "valid_resume.pdf",
        "invalid_file.exe",
        "invalid_file.txt",
        "oversized_file.pdf",
    ]
    # Create files
    create_pdf_file("valid_resume.pdf")
    create_temp_file("invalid_file.exe", size_kb=5)
    create_temp_file("invalid_file.txt", size_kb=5)
    create_temp_file("oversized_file.pdf", size_kb=5120)  # 5MB oversized

    yield  # run tests

    # Cleanup after tests
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def get_upload_input(driver):
    """Returns the file upload input element."""
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "uploadPicture"))
    )


def scroll_and_click(driver, element):
    """Scroll into view and click."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()


# -------------------------------------------------------
# Test Cases
# -------------------------------------------------------

@allure.feature("File Upload")
@allure.story("Valid PDF Upload")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_pdf_upload(driver):
    """
    TC-008: Uploading a valid PDF file should be accepted
    and the filename should appear next to the upload button.
    """
    upload_input = get_upload_input(driver)
    filepath = os.path.abspath("valid_resume.pdf")

    upload_input.send_keys(filepath)

    # Check that the filename appears in the upload element
    uploaded_filename = upload_input.get_attribute("value")
    assert "valid_resume.pdf" in uploaded_filename, \
        "BUG: Valid PDF was not accepted by the file upload field!"


@allure.feature("File Upload")
@allure.story("Invalid File Format - EXE")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_exe_upload(driver):
    """
    TC-009: Uploading an .exe file should either be blocked
    or trigger a validation error. Log as bug if accepted silently.
    """
    upload_input = get_upload_input(driver)
    filepath = os.path.abspath("invalid_file.exe")

    upload_input.send_keys(filepath)

    uploaded_value = upload_input.get_attribute("value")

    # Observation: demoqa may accept it — log this as a real bug finding
    if "invalid_file.exe" in uploaded_value:
        print("[BUG FOUND] BUG-003: .exe file was accepted without validation!")
        allure.attach(
            ".exe file accepted without error — this is a security risk.",
            name="Bug Report: BUG-003",
            attachment_type=allure.attachment_type.TEXT
        )
    else:
        print("[PASS] .exe file was correctly blocked.")


@allure.feature("File Upload")
@allure.story("Invalid File Format - TXT")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_txt_upload(driver):
    """
    TC-010: Uploading a plain .txt file (not a resume format)
    should ideally be rejected. Log as observation if accepted.
    """
    upload_input = get_upload_input(driver)
    filepath = os.path.abspath("invalid_file.txt")

    upload_input.send_keys(filepath)

    uploaded_value = upload_input.get_attribute("value")

    if "invalid_file.txt" in uploaded_value:
        print("[OBSERVATION] TXT file accepted — verify against requirements.")
        allure.attach(
            "Plain .txt file accepted. May be acceptable depending on requirements.",
            name="Observation: TXT Upload",
            attachment_type=allure.attachment_type.TEXT
        )
    else:
        print("[PASS] TXT file was correctly blocked.")


@allure.feature("File Upload")
@allure.story("Oversized File Upload")
@allure.severity(allure.severity_level.CRITICAL)
def test_oversized_file_upload(driver):
    """
    TC-011: Uploading a file larger than the expected size limit (5MB)
    should trigger a size validation error.
    """
    upload_input = get_upload_input(driver)
    filepath = os.path.abspath("oversized_file.pdf")

    upload_input.send_keys(filepath)

    uploaded_value = upload_input.get_attribute("value")

    # Log as bug if oversized file is silently accepted
    if "oversized_file.pdf" in uploaded_value:
        print("[BUG FOUND] BUG-004: Oversized file accepted without size validation!")
        allure.attach(
            "5MB file accepted without any size limit error — potential storage risk.",
            name="Bug Report: BUG-004",
            attachment_type=allure.attachment_type.TEXT
        )
    else:
        print("[PASS] Oversized file was correctly blocked.")


@allure.feature("File Upload")
@allure.story("Empty File Upload Submission")
@allure.severity(allure.severity_level.NORMAL)
def test_submit_without_file_upload(driver):
    """
    TC-012: Submitting the form without uploading a file
    should not cause any errors (upload is optional on this form).
    Verify the form handles missing upload gracefully.
    """
    # Refresh to clear any previous uploads
    driver.get(FORM_URL)

    submit_btn = driver.find_element(By.ID, "submit")
    scroll_and_click(driver, submit_btn)

    # Form should still be on the same page (other required fields will fail)
    assert "automation-practice-form" in driver.current_url, \
        "BUG: Unexpected navigation after submitting with no file uploaded!"
