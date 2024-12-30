import allure
import pytest
from utils.driver_factory import DriverFactory
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="function")
def driver():
    """Fixture for initializing WebDriver."""
    driver = DriverFactory.get_driver()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot on failure."""
    if call.excinfo is not None:
        driver = item.funcargs['driver']
        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Registration Failure Screenshot",
                           attachment_type=allure.attachment_type.PNG)
