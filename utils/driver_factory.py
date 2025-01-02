import undetected_chromedriver as uc
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
            return DriverFactory._get_undetected_chrome_driver()
        raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_undetected_chrome_driver():
        """Set up Undetected-Chromedriver with options."""
        chrome_options = uc.ChromeOptions()

        if Config.HEADLESS:
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Other recommended options for bot detection evasion
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=chrome_options, use_subprocess=True)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        logging.info("Undetected-Chromedriver initialized successfully.")
        return driver
