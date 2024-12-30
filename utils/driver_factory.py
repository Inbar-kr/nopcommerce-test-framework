from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config
import logging

logging.basicConfig(level=logging.INFO)

class DriverFactory:
    @staticmethod
    def get_driver():
        """Initialize WebDriver based on browser and headless settings."""
        browser = Config.BROWSER
        logging.info(f"Initializing WebDriver for {browser} browser.")
        if browser == "chrome":
            return DriverFactory._get_chrome_driver()
        raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_chrome_driver():
        """Set up Chrome WebDriver with options."""
        chrome_options = Options()

        """if Config.HEADLESS:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")"""

        driver_path = ChromeDriverManager().install()

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        logging.info("WebDriver initialized successfully.")
        return driver
