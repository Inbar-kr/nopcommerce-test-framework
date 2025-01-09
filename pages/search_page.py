from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil

class SearchPage(BasePage):
    # Locators for elements on the Search page
    SEARCH_FIELD = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.XPATH, "//button[@class='button-1 search-box-button']")
    SEARCH_KEYWORD_FIELD = (By.ID, "q")
    SEARCH_KEYWORD_BUTTON = (By.XPATH, "//button[@class='button-1 search-button']")
    ERROR_MESSAGE = (By.CLASS_NAME, "no-result")
    ADVANCED_SEARCH_CHECKBOX = (By.ID, "advs")
    SUB_CATEGORIES_SEARCH_CHECKBOX = (By.ID, "isc")
    PRODUCT_DESC_SEARCH_CHECKBOX = (By.ID, "sid")
    PRODUCTS_CONTAINER = (By.CLASS_NAME, "products-container")
    ITEM_GRID = (By.CLASS_NAME, "item-grid")
    PRODUCT_ITEM = (By.CLASS_NAME, "product-item")

    CATEGORY_DROPDOWN = (By.ID, "cid")
    SORT_BY_DROPDOWN = (By.ID, "products-orderby")
    DISPLAY_DROPDOWN = (By.ID, "products-pagesize")

    GRID_VIEW = (By.XPATH, "//a[@data-viewmode='grid']")
    LIST_VIEW = (By.XPATH, "//a[@data-viewmode='list']")

    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "button-2.product-box-add-to-cart-button")
    ADD_TO_WISHLIST_BUTTON = (By.CLASS_NAME, "button-2.add-to-wishlist-button")
    ADD_TO_COMPARE_BUTTON = (By.CLASS_NAME, "button-2.add-to-compare-list-button")

    COMPARE_PRODUCT_LINK = (By.LINK_TEXT, "Compare products list")
    COMPARE_PRODUCT_ERROR = (By.CLASS_NAME, "no-data")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("SearchPage")
        logging.basicConfig(level=logging.INFO)

    def extract_alert_text(self):
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        no_results_message = alert.text
        print("Alert Text:", no_results_message)
        return no_results_message

    def close_popup(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def open_url(self):
        self.driver.get("https://demo.nopcommerce.com/")

    def enter_text(self, field_locator, text: str):
        self.logger.info(f"Entering text '{text}' into field {field_locator}")
        field = self.wait_for_element(field_locator)
        field.clear()
        field.send_keys(text)

    def click(self, locator):
        if isinstance(locator, tuple):
            by, value = locator
            element = self.wait_for_element((by, value))
        else:
            element = self.wait_for_element(locator)

        if element:
            element.click()
            return True
        else:
            self.logger.error(f"Element not found: {locator}")
            return False

    def scroll_to_footer(self):
        self.logger.info("Scrolling down to the footer.")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def wait_for_element(self, locator, timeout=10):
        self.logger.info(f"Waiting for element: {locator}")
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def is_element_visible(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
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
        self.logger.info(f"Fetching elements for locator: {locator}")
        return self.driver.find_elements(*locator)