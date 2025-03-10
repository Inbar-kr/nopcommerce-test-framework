from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import setup_logger

logger = setup_logger()

class WaitUtil:
    @staticmethod
    def wait_for_element(driver, locator, condition, timeout=20):
        """Wait for an element located by the specified locator to satisfy a condition."""
        try:
            logger.debug(f"Waiting for element with locator: {locator}, Condition: {condition}")
            return WebDriverWait(driver, timeout).until(condition(locator))
        except TimeoutException as e:
            logger.error(f"Timeout while waiting for element: {locator}. Exception: {e}")
            raise

    @staticmethod
    def wait_for_element_to_be_visible(driver, locator, timeout=20):
        """Wait for an element located by the specified locator to be visible."""
        return WaitUtil.wait_for_element(driver, locator, EC.visibility_of_element_located, timeout)

    @staticmethod
    def wait_for_element_to_be_clickable(driver, locator, timeout=20):
        """Wait for an element located by the specified locator to be clickable."""
        return WaitUtil.wait_for_element(driver, locator, EC.element_to_be_clickable, timeout)