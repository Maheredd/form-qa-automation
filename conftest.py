import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Base URL of the form being tested
BASE_URL = "https://demoqa.com/automation-practice-form"


# -------------------------------------------------------
# Browser Setup & Teardown
# -------------------------------------------------------

@pytest.fixture(scope="module")
def driver():
    """
    Module-scoped fixture: launches Chrome browser once
    for all tests in a module, then quits after all tests finish.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Uncomment below line to run in headless mode (no browser window)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    driver.implicitly_wait(10)  # wait up to 10s for elements to appear

    yield driver  # hand driver to the test

    driver.quit()  # cleanup after all tests in the module


@pytest.fixture(scope="function")
def fresh_driver():
    """
    Function-scoped fixture: launches a fresh browser for EACH test.
    Use this when tests must not share browser state.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


# -------------------------------------------------------
# Screenshot on Failure
# -------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically captures a screenshot and attaches it
    to the Allure report whenever a test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get the driver from the test's fixtures
        driver = item.funcargs.get("driver") or item.funcargs.get("fresh_driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )


# -------------------------------------------------------
# Base URL fixture (optional helper)
# -------------------------------------------------------

@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for use in any test."""
    return BASE_URL
