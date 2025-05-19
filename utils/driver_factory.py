import undetected_chromedriver as uc
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from config.config import Config
from selenium import webdriver
import logging
import os

logging.basicConfig(level=logging.INFO)

class DriverFactory:
    @staticmethod
    def get_driver(browser: str, headless: bool):
        browser = browser.lower()

        logging.info(f"Initializing WebDriver for '{browser}' browser. Headless mode: {headless}")

        if browser == "chrome":
            return DriverFactory._get_undetected_chrome_driver(headless)
        if browser == "firefox":
            return DriverFactory._get_firefox_driver(headless)

        raise ValueError(f"Unsupported browser: {browser}")


    @staticmethod
    def _get_undetected_chrome_driver(headless):
        chrome_options = uc.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")

        driver = uc.Chrome(options=chrome_options, use_subprocess=True)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        return driver

    @staticmethod
    def _get_firefox_driver(headless):
        firefox_options = webdriver.FirefoxOptions()

        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.set_preference("layout.css.devPixelsPerPx", "1.0")
        firefox_options.set_preference("dom.webnotifications.enabled", False)

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        return driver