import allure
import pytest
from utils.driver_factory import DriverFactory
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define the path for screenshots
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    headless = False

    driver = DriverFactory.get_driver(browser, headless)
    driver.maximize_window()
    yield driver
    driver.quit()



@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.excinfo is not None:
        driver = item.funcargs['driver']
        screenshot_filename = f"screenshot_{os.getenv('BROWSER', 'test')}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)

        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
