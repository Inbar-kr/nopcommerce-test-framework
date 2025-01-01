import os
from webdriver_manager.chrome import ChromeDriverManager

def str_to_bool(value):
    return value.lower() in ("true", "1", "t", "y", "yes")

class Config:
    # Base URL for the application under test
    BASE_URL = os.getenv("BASE_URL", "https://demo.nopcommerce.com/")

    # WebDriver settings
    BROWSER = os.getenv("BROWSER", "chrome")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 20))

    # Headless setting (for running tests without a UI)
    HEADLESS = str_to_bool(os.getenv("HEADLESS", "False"))

    # Test data file path
    TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "testdata.json")
    if not os.path.exists(TEST_DATA_PATH):
        raise FileNotFoundError(f"Test data file not found at {TEST_DATA_PATH}")

    # Reporting settings
    REPORTS_DIR = os.getenv("REPORTS_DIR", "./reports")
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    # Screenshot settings
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "./screenshots")
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    SCREENSHOT_ON_FAILURE = str_to_bool(os.getenv("SCREENSHOT_ON_FAILURE", "True"))

    # WebDriver settings
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", os.path.join(os.path.dirname(__file__), "drivers", "chromedriver.exe"))

    @staticmethod
    def get_chrome_driver_path():
        if not os.path.exists(Config.CHROME_DRIVER_PATH):
            # Fallback to WebDriverManager if chromedriver.exe is missing
            from webdriver_manager.chrome import ChromeDriverManager
            return ChromeDriverManager().install()
        return Config.CHROME_DRIVER_PATH

    # Environment settings (useful for staging, production, etc.)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")

    # Credentials (ensure secure handling)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin@example.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "securepassword")