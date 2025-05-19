import allure
import pytest
from utils.driver_factory import DriverFactory
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define the path for screenshots
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = DriverFactory.get_driver(browser, headless)
    driver.maximize_window()
    yield driver
    driver.quit()



@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.excinfo is not None and 'driver' in item.funcargs:
        driver = item.funcargs['driver']
        browser = os.getenv('BROWSER', 'unknown')
        screenshot_filename = f"screenshot_{item.name}_{browser}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)

        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
