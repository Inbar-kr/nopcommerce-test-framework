import undetected_chromedriver as uc
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from config.config import Config
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO)

class DriverFactory:
    @staticmethod
    def get_driver():
        """Initialize WebDriver based on browser and headless settings."""
        browser = Config.BROWSER
        logging.info(f"Initializing WebDriver for {browser} browser.")

        if browser == "chrome":
            return DriverFactory._get_undetected_chrome_driver()

        if browser == "firefox":
            return DriverFactory._get_firefox_driver()

        raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_undetected_chrome_driver():
        """Set up Undetected-Chromedriver with options."""
        chrome_options = uc.ChromeOptions()

        if Config.HEADLESS:
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=chrome_options, use_subprocess=True)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        logging.info("Undetected-Chromedriver initialized successfully.")
        return driver

    @staticmethod
    def _get_firefox_driver():
        """Set up Firefox with webdriver-manager."""
        firefox_options = webdriver.FirefoxOptions()

        if Config.HEADLESS:
            # firefox_options.add_argument("--headless")
            firefox_options.add_argument("--disable-gpu")

        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")

        firefox_service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        logging.info("Firefox driver initialized successfully.")
        return driver
