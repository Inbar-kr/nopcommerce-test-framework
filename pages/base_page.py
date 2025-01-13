from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)


    def open_url(self, url):
        self.driver.get(url)
        self.logger.info(f"Opened URL: {url}")

    def enter_text(self, locator, text: str):
        self.logger.info(f"Entering text '{text}' into field: {locator}")
        field = self.wait_for_element(locator)
        field.clear()
        field.send_keys(text)
        self.logger.info(f"Text entered into field: {locator}")

    def click(self, locator):
        if isinstance(locator, tuple):
            by, value = locator
            element = self.wait_for_element((by, value))
        else:
            element = self.wait_for_element(locator)

        if element:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"Clicked on element: {locator}")
                return True
            except Exception as e:
                self.logger.error(f"Error clicking element: {locator} - {str(e)}")
                return False
        else:
            self.logger.error(f"Element not found: {locator}")
            return False

    def extract_alert_text(self):
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        self.logger.info(f"Alert Text: {alert_text}")
        return alert_text

    def close_popup(self):
        alert = self.driver.switch_to.alert
        alert.accept()
        self.logger.info("Popup closed.")

    def scroll_to_footer(self):
        self.logger.info("Scrolling down to the footer.")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_into_view(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info("Scrolled element into view.")
        except Exception as e:
            self.logger.error(f"Error scrolling element into view: {str(e)}")

    def wait_for_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {locator}")
            raise TimeoutException(f"Timeout waiting for element: {locator}")

    def is_element_visible(self, locator, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            return any(element.is_displayed() for element in elements)
        except:
            self.logger.error(f"Element not visible: {locator}")
            return False

    def wait_for_placeholder(self, driver, field_locator, expected_placeholder, timeout=10):
        self.logger.info(f"Waiting for placeholder on field: {field_locator}")
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(field_locator)
            )
            actual_placeholder = element.get_attribute("placeholder")
            assert actual_placeholder == expected_placeholder, f"Expected placeholder '{expected_placeholder}', but got '{actual_placeholder}'."
            self.logger.info(f"Placeholder for field {field_locator} is correct: '{expected_placeholder}'")
        except Exception as e:
            self.logger.error(f"Error occurred while checking placeholder: {str(e)}")
            raise

    def validate_placeholder(self, field_locator, expected_placeholder):
        field_element = self.wait_for_element(field_locator)
        actual_placeholder = field_element.get_attribute("placeholder")
        self.logger.info(f"Placeholder for {field_locator}: '{actual_placeholder}'")

        assert actual_placeholder == expected_placeholder, \
            f"Expected placeholder for field '{field_locator}' to be '{expected_placeholder}', but found '{actual_placeholder}'"
        self.logger.info(f"Placeholder for field '{field_locator}' is correct: '{actual_placeholder}'")


    def select_dropdown_option(self, dropdown_locator, option_text: str):
        try:
            dropdown_element = self.wait_for_element(dropdown_locator)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(dropdown_element))

            select = Select(dropdown_element)

            self.logger.info(f"Dropdown options before selecting: {[option.text for option in select.options]}")

            select.select_by_visible_text(option_text)
            self.logger.info(f"Selected '{option_text}' from dropdown.")

        except Exception as e:
            self.logger.error(f"Error selecting option '{option_text}' from dropdown: {str(e)}")
            raise

    def get_elements(self, locator):
        elements = self.driver.find_elements(*locator)
        if not elements:
            self.logger.error(f"No elements found for locator: {locator}")
        else:
            self.logger.info(f"Found {len(elements)} elements for locator: {locator}")
        return elements

    def get_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {locator}")
            raise TimeoutException(f"Timeout waiting for element: {locator}")

    def get_text_value(self, locator):
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(locator),
            )

            if element.tag_name in ["input", "textarea", "select"]:
                return element.get_attribute("value")
            else:
                return element.text.strip()

        except TimeoutException:
            self.logger.error(f"Timeout while waiting for element with locator {locator}")
            raise

    def get_selected_option(self, dropdown_locator):
        dropdown = self.find_element(dropdown_locator)
        return Select(dropdown).first_selected_option.text

    def find_element(self, locator, timeout=20):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator),
            )
        except TimeoutException:
            self.logger.error(f"Element with locator {locator} not found within {timeout} seconds.")
            raise TimeoutException(f"Element with locator {locator} not found within {timeout} seconds.")

    def get_element_text(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Extracted text: '{text}' from element: {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"Element with locator {locator} not found within {timeout} seconds.")
            raise TimeoutException(f"Element with locator {locator} not found within {timeout} seconds.")

