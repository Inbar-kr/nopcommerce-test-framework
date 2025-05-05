from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
import time

class SearchPage(BasePage):
    # --- Locators ---
    SEARCH_FIELD = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.XPATH, "//button[@class='button-1 search-box-button']")
    SEARCH_KEYWORD_FIELD = (By.ID, "q")
    SEARCH_KEYWORD_BUTTON = (By.XPATH, "//button[@class='button-1 search-button']")
    ERROR_MESSAGE = (By.CLASS_NAME, "no-result")
    DESCRIPTION_FIELD = (By.CLASS_NAME, "full-description")
    ADVANCED_SEARCH_CHECKBOX = (By.ID, "advs")
    SUB_CATEGORIES_SEARCH_CHECKBOX = (By.ID, "isc")
    PRODUCT_DESC_SEARCH_CHECKBOX = (By.ID, "sid")
    PRODUCTS_CONTAINER = (By.CLASS_NAME, "products-container")
    ITEM_GRID = (By.CLASS_NAME, "item-grid")
    PRODUCT_ITEM = (By.CSS_SELECTOR, ".product-item")

    CATEGORY_DROPDOWN = (By.ID, "cid")
    SORT_BY_DROPDOWN = (By.ID, "products-orderby")
    DISPLAY_DROPDOWN = (By.ID, "products-pagesize")
    CURRENT_PAGE_BUTTON = (By.CLASS_NAME, "current-page")
    INDIVIDUAL_PAGE_BUTTON = (By.CLASS_NAME, "individual-page")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, "li.next-page a")
    PREVIOUS_PAGE_BUTTON = (By.CSS_SELECTOR, "li.previous-page a")

    # View modes
    GRID_VIEW = (By.XPATH, "//a[@data-viewmode='grid']")
    LIST_VIEW = (By.XPATH, "//a[@data-viewmode='list']")

    # Buttons
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "button-2.product-box-add-to-cart-button")
    ADD_TO_WISHLIST_BUTTON = (By.CLASS_NAME, "button-2.add-to-wishlist-button")
    ADD_TO_COMPARE_BUTTON = (By.CLASS_NAME, "button-2.add-to-compare-list-button")

    # Compare products
    COMPARE_PRODUCT_LINK = (By.LINK_TEXT, "Compare products list")
    COMPARE_PRODUCT_ERROR = (By.CLASS_NAME, "no-data")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("SearchPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self, url="https://demo.nopcommerce.com/"):
        self.driver.get(url)

    # Search and Validation
    def _search_for_product(self, search_data):
        self.enter_text(self.SEARCH_FIELD, search_data)
        self.click(self.SEARCH_BUTTON)
        self.logger.info(f"Searching for product: {search_data}")

    def _validate_search_results(self, search_data):
        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."
        assert any(search_data in result.text for result in search_results), \
            f"The product '{search_data}' is not found in the search results."

    def _validate_error_message(self):
        error_locator = self.ERROR_MESSAGE
        assert self.is_element_visible(error_locator[0], error_locator[1]), \
            "No products found for the invalid product."
        self.logger.info("Error message for invalid product displayed.")

    def _validate_multiple_products_found(self, locator):
        product_items = self.get_elements(locator)
        assert len(product_items) > 1, "Search results did not return multiple products."
        self.logger.info(f"Found {len(product_items)} products in search results.")

    def _validate_product_description(self, search_data_description):
        self.wait_for_element(self.DESCRIPTION_FIELD)
        full_description = self.driver.find_element(By.CLASS_NAME, "full-description").text

        assert search_data_description in full_description, \
            f"The product description does not contain '{search_data_description}'. Full description found: {full_description}"
        self.logger.info("Validated product description successfully.")

    def _search_with_category(self, product, category):
        self.open_url()
        self.enter_text(self.SEARCH_FIELD, product)
        self.click(self.SEARCH_BUTTON)

        self.enter_text(self.SEARCH_KEYWORD_FIELD, product)
        self.click(self.ADVANCED_SEARCH_CHECKBOX)
        self.select_dropdown_option(self.CATEGORY_DROPDOWN, category)
        self.click(self.SEARCH_KEYWORD_BUTTON)
        self.logger.info(f"Search for product '{product}' with category '{category}' executed.")

    def search_valid_product(self, load_test_data):
        search_data = load_test_data["product_search"]["valid_product"]
        self.open_url()
        self._search_for_product(search_data)

        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."
        assert any(search_data in result.text for result in search_results), \
            f"The product '{search_data}' is not found in the search results."

        self.logger.info(f"Successfully searched for valid product: {search_data}")

    def search_invalid_product(self, load_test_data):
        test_data = load_test_data["product_search"]["invalid_product"]
        self.open_url()
        self._search_for_product(test_data)

        assert self.is_element_visible(self.ERROR_MESSAGE[0], self.ERROR_MESSAGE[1]), \
            "Error message for no products found not displayed."

        self.logger.info(f"Attempted to search for invalid product: {test_data}")

    def empty_search(self):
        self.open_url()
        self._search_for_product("")

        alert_text = self.extract_alert_text()
        expected_message = "Please enter some search keyword"

        self.assert_alert_message(alert_text, expected_message)
        self.close_popup()

        self.logger.info("Attempted to search for empty search products.")

    def search_multiple_products(self, load_test_data):
        search_data = load_test_data["multiple_products_search"]["multiple_products"]
        self.open_url()
        self._search_for_product(search_data)

        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 1, "Less than two products found in the search results."
        assert any(search_data in result.text for result in search_results), \
            f"The product '{search_data}' is not found in the search results."

        self.logger.info(f"Attempted to search for multiple products: {search_data}")

    def search_using_search_keyboard_field(self, driver, load_test_data):
        invalid_product = load_test_data["product_search"]["invalid_product"]
        self.open_url()
        self._search_for_product(invalid_product)
        self._validate_error_message()

        valid_product = load_test_data["product_search"]["valid_product"]
        self.enter_text(self.SEARCH_KEYWORD_FIELD, valid_product)
        self.click(self.SEARCH_KEYWORD_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."
        assert any(valid_product in result.text for result in search_results), \
            f"The product '{valid_product}' is not found in the search results."

        self.logger.info("Search completed successfully using the search keyword field.")

    def search_using_keyboard_keys(self, driver, load_test_data):
        search_data_valid = load_test_data["product_search"]["valid_product"]

        self.open_url()

        search_field = driver.find_element(*SearchPage.SEARCH_FIELD)
        search_field.send_keys(search_data_valid)

        search_field.send_keys(Keys.TAB)
        search_field.send_keys(Keys.ENTER)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."

        assert any(search_data_valid in result.text for result in search_results), \
            f"The product '{search_data_valid}' is not found in the search results."

        self.logger.info("Attempted to search using keyboard keys.")


    # Product Interaction
    def _click_first_product_in_results(self):
        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert search_results, "No search results available"
        first_product = search_results[0]
        first_product.find_element(By.CLASS_NAME, "picture").click()
        self.logger.info("Clicked on the first product in search results.")

    def select_first_product(self):
        self.wait_for_element(self.ITEM_GRID)
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        assert products, "No products found in the item grid."
        self.logger.info(f"Found {len(products)} product(s) in grid.")
        products[0].find_element(By.CLASS_NAME, "picture").click()
        self.logger.info("Clicked the first product.")

    def search_with_description(self, search_text):
        self.enter_text(self.SEARCH_FIELD, search_text)
        self.click(self.SEARCH_BUTTON)
        self.logger.info(f"Entered search text: {search_text}")

        self.click(self.ADVANCED_SEARCH_CHECKBOX)
        self.click(self.PRODUCT_DESC_SEARCH_CHECKBOX)
        self.click(self.SEARCH_KEYWORD_BUTTON)
        self.logger.info("Enabled advanced search with product description.")

    def add_products_to_compare(self):
        product_items = self.get_elements((By.CLASS_NAME, "product-item"))
        assert len(product_items) > 1, "Less than two products found for comparison."

        product_items[0].find_element(*self.ADD_TO_COMPARE_BUTTON).click()
        time.sleep(2)
        product_items[1].find_element(*self.ADD_TO_COMPARE_BUTTON).click()
        time.sleep(2)

    def navigate_to_compare_page(self):
        self.click(self.COMPARE_PRODUCT_LINK)
        WebDriverWait(self.driver, 10).until(EC.url_contains("compare"))
        assert "compare" in self.driver.current_url, "User was not navigated to the Product Compare Page."

    def validate_compare_page_display(self):
        compare_product_items = self.get_elements((By.XPATH, "//tr[contains(@class, 'product-name') or "
                                                             "contains(@class, 'product-price') or "
                                                             "contains(@class, 'specification')]"))
        visible_items = [item for item in compare_product_items if item.is_displayed()]
        assert len(visible_items) >= 2, "Less than two visible products are displayed in the Compare page."

        self.logger.info("Successfully validated the products on the compare page.")


    # Sorting and Filtering
    def apply_sort_option_and_validate(self, option):
        self.select_dropdown_option(self.SORT_BY_DROPDOWN, option)
        time.sleep(2)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "price"))
        )

        product_items = self.get_elements(self.PRODUCT_ITEM)

        product_names = [
            product.find_element(By.CLASS_NAME, "product-title").text
            for product in product_items
        ]
        product_prices = [
            float(product.find_element(By.CLASS_NAME, "prices")
                  .find_element(By.CLASS_NAME, "actual-price")
                  .text.replace("$", "").replace(",", ""))
            for product in product_items
        ]

        self.logger.info(f"Product Names: {product_names}")
        self.logger.info(f"Product Prices: {product_prices}")

        if option == "Price: Low to High":
            expected = sorted(product_prices)
            assert product_prices == expected, f"Expected {expected}, got {product_prices}"
        elif option == "Price: High to Low":
            expected = sorted(product_prices, reverse=True)
            assert product_prices == expected, f"Expected {expected}, got {product_prices}"
        elif option == "Name: A to Z":
            expected = sorted(product_names)
            assert product_names == expected, f"Expected {expected}, got {product_names}"
        elif option == "Name: Z to A":
            expected = sorted(product_names, reverse=True)
            assert product_names == expected, f"Expected {expected}, got {product_names}"
        elif option == "Created on":
            self.logger.info("Sorting by 'Created on' is not implemented.")
            return

        self.logger.info(f"Sorting validated successfully for option: {option}")

    def search_by_category(self, load_test_data):
        valid_product = load_test_data["product_search"]["valid_product"]
        valid_category = "Computers >> Notebooks"
        invalid_category = "Apparel"

        self._search_with_category(valid_product, valid_category)
        self._validate_search_results(valid_product)

        self._search_with_category(valid_product, invalid_category)
        self._validate_error_message()

        self.logger.info("Attempted to search products by category.")

    def search_in_subcategories(self, load_test_data):
        valid_product = load_test_data["product_search"]["valid_product"]
        valid_category = "Computers"

        self._search_with_category(valid_product, valid_category)
        self._validate_error_message()

        self.click(self.SUB_CATEGORIES_SEARCH_CHECKBOX)
        self.click(self.SEARCH_KEYWORD_BUTTON)

        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found when searching with subcategories enabled."
        self.logger.info("Successfully searched with subcategory filter enabled.")

    def validate_placeholders(self, driver):
        self.open_url()

        expected_placeholders = {self.SEARCH_FIELD: "Search store"}

        for field_locator, expected_placeholder in expected_placeholders.items():
            self._validate_placeholder_for_field(driver, field_locator, expected_placeholder)


    # Views and Display
    def open_search_results(self, search_text):
        self.open_url("https://demo.nopcommerce.com/")
        self.enter_text((By.ID, "small-searchterms"), search_text)
        self.click((By.XPATH, "//button[@class='button-1 search-box-button']"))
        self.wait_for_element(self.PRODUCT_ITEM)

    def validate_product_display(self, driver, view_mode):
        self.click(view_mode)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
        )

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) == 1, f"{view_mode} view did not display a single product as expected."

        assert self.is_element_visible(*self.ADD_TO_CART_BUTTON), "Add to Cart option missing."
        assert self.is_element_visible(*self.ADD_TO_WISHLIST_BUTTON), "Wish List option missing."
        assert self.is_element_visible(*self.ADD_TO_COMPARE_BUTTON), "Compare Product option missing."

        self.logger.info("view mode displays a single product with required options.")

    def list_and_grid_views(self, driver, load_test_data):
        search_single_product = load_test_data["product_search"]["valid_product"]
        search_multiple_products = load_test_data["multiple_products_search"]["multiple_products"]

        self.logger.info("Searching for a single product.")
        self.open_url()
        self.enter_text(SearchPage.SEARCH_FIELD, search_single_product)
        self.click(SearchPage.SEARCH_BUTTON)

        self.validate_product_display(driver, SearchPage.GRID_VIEW)
        self.validate_product_display(driver, SearchPage.LIST_VIEW)

        self.logger.info("Both Grid and List view modes display a single product with required options.")

        self.logger.info("Searching for multiple products.")
        self.open_url()
        self.enter_text(SearchPage.SEARCH_FIELD, search_multiple_products)
        self.click(SearchPage.SEARCH_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Multiple products not displayed as expected in the search results."
        self.logger.info(f"Multiple products displayed: {len(product_items)} found.")

    def pages_views_products(self, driver, load_test_data):
        search_multiple_products = load_test_data["multiple_products_search"]["multiple_products"]

        self.logger.info("Searching for multiple products.")
        self.open_url()
        self.enter_text(self.SEARCH_FIELD, search_multiple_products)
        self.click(self.SEARCH_BUTTON)

        self.scroll_to_footer()

        self.click(self.NEXT_PAGE_BUTTON)
        self.click(self.PREVIOUS_PAGE_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Multiple products not displayed as expected in the search results."
        self.logger.info(f"Multiple products displayed: {len(product_items)} found.")

    def display_number_of_products(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]
        display_options = ["3", "6", "9", "18"]

        self.open_url()

        self.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        self.click(SearchPage.SEARCH_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Search did not return multiple products as expected."

        for option in display_options:
            self.select_dropdown_option(SearchPage.DISPLAY_DROPDOWN, option)

            time.sleep(3)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
            )

            product_items = driver.find_elements(By.CLASS_NAME, "product-item")
            assert len(product_items) <= int(
                option), f"Expected up to {option} products, but found {len(product_items)}."

        self.logger.info("Attempted to display the number of products as expected.")

    def search_box_displayed_on_all_pages(self, driver):
        pages_to_test = [
            "/computers", "/electronics", "/apparel", "/digital-downloads",
            "/books", "/jewelry", "/gift-cards", "/desktops", "/notebooks",
            "/software", "/camera-photo", "/cell-phones", "/others",
            "/shoes", "/clothing", "/accessories"
        ]

        self.open_url()

        for page in pages_to_test:
            driver.get(f"{driver.current_url}{page}")

            search_box = driver.find_element(By.ID, "small-searchterms")
            search_button = driver.find_element(By.XPATH, "//button[@class='button-1 search-box-button']")

            assert search_box.is_displayed(), f"Search textbox is not displayed on {page}."
            assert search_button.is_displayed(), f"Search button is not displayed on {page}."

        self.logger.info("Attempted to display the search box on all the pages.")

    # Helper Functions
    def _validate_placeholder_for_field(self, driver, field_locator, expected_placeholder):
        field = self.wait_for_element(field_locator, timeout=10)
        if field:
            actual_placeholder = field.get_attribute("placeholder")
            assert actual_placeholder == expected_placeholder, \
                f"Placeholder mismatch! Expected: '{expected_placeholder}', but got: '{actual_placeholder}'"
            self.logger.info(f"Placeholder for field '{field_locator}' is correct.")
        else:
            self.logger.error(f"Field '{field_locator}' not found.")

    def navigate_from_sitemap(self, driver):
        self.open_url()
        self.scroll_to_footer()

        sitemap_link = driver.find_element(By.LINK_TEXT, "Sitemap")
        sitemap_link.click()

        search_link = driver.find_element(By.LINK_TEXT, "Search")
        search_link.click()

        current_url = driver.current_url
        assert "search" in current_url, f"User was not navigated to the 'Search' page. Current URL: {current_url}"
        self.logger.info(f"User successfully navigated to the Search page. Current URL: {current_url}")

    def heading_url_and_title(self, driver, load_test_data):
        search_data_valid = load_test_data["product_search"]["valid_product"]

        self.open_url()

        self.enter_text(SearchPage.SEARCH_FIELD, search_data_valid)
        self.click(SearchPage.SEARCH_BUTTON)

        page_heading = driver.find_element(By.CSS_SELECTOR, ".page-title h1").text
        assert page_heading == "Search", f"Expected page heading 'Search', but got '{page_heading}'."

        page_url = driver.current_url
        assert "search" in page_url, f"Expected URL to contain 'search', but got '{page_url}'."

        page_title = driver.title
        assert "Search" in page_title, f"Expected page title to contain 'Search', but got '{page_title}'."

        self.logger.info("Attempted to search using keyboard keys.")
