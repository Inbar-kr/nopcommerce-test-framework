import time
import pytest
import json
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from pages.search_page import SearchPage
from config.config import Config
from allure_commons.types import Severity
from tests.test_login import TestUserLogin

@pytest.fixture(scope="module")
def load_test_data():
    with open(Config.TEST_DATA_PATH, 'r') as f:
        return json.load(f)

@allure.epic("Product Management")
@allure.feature("Search")
class TestUserSearch:

    @allure.story("TC_SF_001: Validate searching with an existing Product Name")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates that searching for an existing product displays the correct product in the search results.")
    def test_valid_product(self, driver, load_test_data):
        search_data = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_data)

        search_page.click(SearchPage.SEARCH_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."

        assert any(search_data in result.text for result in search_results), \
            f"The product '{search_data}' is not found in the search results."

    @allure.story("TC_SF_002: Validate searching with a non-existing Product Name")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test validates that searching for a non-existing product displays an appropriate message.")
    def test_invalid_product_search(self, driver, load_test_data):
        test_data = load_test_data["product_search"]["invalid_product"]

        search_page = SearchPage(driver)

        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, test_data)

        search_page.click(SearchPage.SEARCH_BUTTON)


        error_locator = (By.CLASS_NAME, "no-result")

        assert search_page.is_element_visible(error_locator), \
            "Search failed. Error message for no products found not displayed."

    @allure.story("TC_SF_003: Validate searching without providing any Product Name")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test validates that searching without entering a product name displays an appropriate popup message.")
    def test_empty_product_search(self, driver):
        search_page = SearchPage(driver)

        search_page.open_url()

        search_page.click(SearchPage.SEARCH_BUTTON)

        alert_text = search_page.extract_alert_text()
        expected_message = "Please enter some search keyword"

        time.sleep(2)

        assert alert_text == expected_message, \
            f"Unexpected alert message: '{alert_text}'. Expected: '{expected_message}'"

        search_page.close_popup()

    @allure.story("TC_SF_004: Validate searching for a product after login to the Application")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for an existing product after logging in displays the correct product in the search results.")
    def test_search_product_after_login(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        test_data = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)

        search_page.enter_text(SearchPage.SEARCH_FIELD, test_data)
        search_page.click(SearchPage.SEARCH_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."
        time.sleep(2)

        assert any(test_data in result.text for result in search_results), \
            f"The product '{test_data}' is not found in the search results."

    @allure.story("TC_SF_005: Validate searching by providing a search criteria which results in multiple products")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching with a criteria that returns multiple products displays more than one product in the search results.")
    def test_search_multiple_products(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)

        search_page.click(SearchPage.SEARCH_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 1, "Less than two products found in the search results."

    @allure.story("TC_SF_006: Validate all the fields in the Search functionality and Search page have placeholders")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test verifies that all fields on the Search page have the correct placeholder text.")
    def test_search_field_placeholders(self, driver):
        search_page = SearchPage(driver)
        search_page.open_url()

        expected_placeholders = {search_page.SEARCH_FIELD: "Search store"}

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = search_page.wait_for_element(field_locator, timeout=10)
            if field:
                search_page.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                print(f"Field {field_locator} not found!")
        print("All search fields have the correct placeholders.")

    @allure.story("TC_SF_007: Validate searching using 'Search keyword' field")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching using the 'Search keyword' field works and displays the correct product in the search results.")
    def test_search_using_keyword_field(self, driver, load_test_data):
        search_data_invalid = load_test_data["product_search"]["invalid_product"]
        search_data_valid = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_data_invalid)
        search_page.click(SearchPage.SEARCH_BUTTON)

        error_locator = (By.CLASS_NAME, "no-result")
        assert search_page.is_element_visible(error_locator), "No products found for the invalid product."

        search_page.enter_text(SearchPage.SEARCH_KEYWORD_FIELD, search_data_valid)
        search_page.click(SearchPage.SEARCH_KEYWORD_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."

        assert any(search_data_valid in result.text for result in search_results), \
            f"The product '{search_data_valid}' is not found in the search results."

    @allure.story("TC_SF_008: Validate Search using the text from the product description")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for a product using text from its description returns the correct product in the search results.")
    def test_search_using_product_description(self, driver, load_test_data):
        search_data_description = load_test_data["product_description_search"]["product_description_text"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_data_description)
        search_page.click(SearchPage.SEARCH_BUTTON)

        search_page.wait_for_element(SearchPage.ITEM_GRID)
        search_results = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(search_results) > 0, "No products found using the description text."

        first_product = search_results[0]
        first_product.find_element(By.CLASS_NAME, "picture").click()

        search_page.wait_for_element((By.CLASS_NAME, "full-description"))
        full_description = driver.find_element(By.CLASS_NAME, "full-description").text

        assert search_data_description in full_description, \
            f"The product description does not contain '{search_data_description}'. Full description found: {full_description}"
    @allure.story("TC_SF_009: Validate Search by selecting the category of product")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for a product by selecting the correct or incorrect category returns the expected results.")
    def test_search_by_category(self, driver, load_test_data):
        valid_product = load_test_data["product_search"]["valid_product"]
        valid_category = "Computers"
        invalid_category = "Apparel"

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, valid_product)
        search_page.click(SearchPage.SEARCH_BUTTON)

        search_page.enter_text(SearchPage.SEARCH_KEYWORD_FIELD, valid_product)

        search_page.click(SearchPage.ADVANCED_SEARCH_CHECKBOX)

        search_page.select_dropdown_option(SearchPage.CATEGORY_DROPDOWN, valid_category)
        search_page.click(SearchPage.SUB_CATEGORIES_SEARCH_CHECKBOX)

        search_page.click(SearchPage.SEARCH_KEYWORD_BUTTON)
        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "Product not found with the correct category selection."

        # Repeat search with incorrect category
        search_page.enter_text(SearchPage.SEARCH_KEYWORD_FIELD, valid_product)
        search_page.select_dropdown_option(SearchPage.CATEGORY_DROPDOWN, invalid_category)
        search_page.click(SearchPage.SEARCH_KEYWORD_BUTTON)

        error_message_locator = SearchPage.ERROR_MESSAGE
        assert search_page.is_element_visible(error_message_locator), \
            "'No products were found that matched your criteria' message not displayed."

    @allure.story("TC_SF_010: Validate Search by selecting to search in subcategories")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that searching with the 'Automatically search subcategories' option enabled returns the expected results.")
    def test_search_in_subcategories(self, driver, load_test_data):
        valid_product = load_test_data["product_search"]["valid_product"]
        valid_parent_category = "Computers"

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, valid_product)
        search_page.click(SearchPage.SEARCH_BUTTON)
        search_page.click(SearchPage.ADVANCED_SEARCH_CHECKBOX)

        search_page.select_dropdown_option(SearchPage.CATEGORY_DROPDOWN, valid_parent_category)
        search_page.click(SearchPage.SEARCH_KEYWORD_BUTTON)

        error_message_locator = SearchPage.ERROR_MESSAGE
        assert search_page.is_element_visible(error_message_locator), \
            "'No products were found that matched your criteria' message not displayed when using parent category only."
        time.sleep(2)

        search_page.click(SearchPage.SUB_CATEGORIES_SEARCH_CHECKBOX)
        search_page.click(SearchPage.SEARCH_KEYWORD_BUTTON)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found when searching with subcategories enabled."

    @allure.story("TC_SF_011: Validate List and Grid views when only one Product is displayed in the search results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the List and Grid views for a single product displayed in the search results and verifies navigation to the Product Display Page.")
    def test_list_and_grid_views_single_product(self, driver, load_test_data):
        search_criteria = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        search_page.click(SearchPage.SEARCH_BUTTON)

        def validate_product_display(view_mode):
            search_page.click(view_mode)
            time.sleep(2)

            product_items = driver.find_elements(By.CLASS_NAME, "product-item")

            assert len(product_items) == 1, f"{view_mode} view did not display a single product as expected."

            assert search_page.is_element_visible(SearchPage.ADD_TO_CART_BUTTON), "Add to Cart option missing."
            assert search_page.is_element_visible(SearchPage.ADD_TO_WISHLIST_BUTTON), "Wish List option missing."
            assert search_page.is_element_visible(SearchPage.ADD_TO_COMPARE_BUTTON), "Compare Product option missing."

        # Validate ER-1: Single product displayed in Grid view
        validate_product_display(SearchPage.GRID_VIEW)

        # Validate ER-2: Single product displayed in List view
        validate_product_display(SearchPage.LIST_VIEW)

    @allure.story("TC_SF_012: Validate List and Grid views when multiple Products are displayed in the search results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the List and Grid views for multiple products displayed in the search results and verifies navigation to the Product Display Page for each product.")
    def test_list_and_grid_views_multiple_products(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        search_page.click(SearchPage.SEARCH_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Less than two products found for the search criteria."

        def validate_product_display(view_mode):
            # Switch to the specified view mode (List or Grid)
            search_page.click(view_mode)
            time.sleep(2)

            product_items = driver.find_elements(By.CLASS_NAME, "product-item")
            assert len(product_items) > 1, f"{view_mode} view did not display multiple products as expected."

            for product in product_items:
                assert search_page.is_element_visible(SearchPage.ADD_TO_CART_BUTTON), "Add to Cart option missing."
                assert search_page.is_element_visible(SearchPage.ADD_TO_WISHLIST_BUTTON), "Wish List option missing."
                assert search_page.is_element_visible(SearchPage.ADD_TO_COMPARE_BUTTON), "Compare Product option missing."

        # Validate ER-1: Single product displayed in Grid view
        validate_product_display(SearchPage.GRID_VIEW)

        # Validate ER-2: Single product displayed in List view
        validate_product_display(SearchPage.LIST_VIEW)

    @allure.story("TC_SF_013: Validate adding to Product Compare Page from Search Results page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that products can be added to the compare list from the search results page and verifies that the user is navigated to the Product Compare Page.")
    def test_add_to_compare_page_from_search_results(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        search_page.click(SearchPage.SEARCH_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Less than two products found for comparison."

        product_items[0].find_element(*SearchPage.ADD_TO_COMPARE_BUTTON).click()
        time.sleep(2)

        product_items[1].find_element(*SearchPage.ADD_TO_COMPARE_BUTTON).click()
        time.sleep(2)

        search_page.click(SearchPage.COMPARE_PRODUCT_LINK)
        assert "compare" in driver.current_url, "User was not navigated to the Product Compare Page."


        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tr.product-picture")))

        compare_product_items = driver.find_elements(By.XPATH,
                                                     "//tr[contains(@class, 'product-name') or contains(@class, 'product-price') or contains(@class, 'specification')]")
        visible_items = [item for item in compare_product_items if item.is_displayed()]

        assert len(visible_items) >= 2, "Less than two visible products are displayed in the Compare page."

    @allure.story("TC_SF_014: Validate User is able to sort the Products displayed in the Search Results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that products can be sorted according to the selected option from the 'Sort By' dropdown on the Search Results page.")
    def test_sort_products_in_search_results(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]
        sort_options = load_test_data.get("sort_options", [])
        assert sort_options, "Sort options list is empty."

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        search_page.click(SearchPage.SEARCH_BUTTON)

        product_items = search_page.get_elements(SearchPage.PRODUCT_ITEM)
        assert len(product_items) > 1, "Search results did not return multiple products."


        for option in sort_options:
            search_page.select_dropdown_option(SearchPage.SORT_BY_DROPDOWN, option)

            time.sleep(3)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "price"))
            )

            product_items = search_page.get_elements(SearchPage.PRODUCT_ITEM)

            product_names = [
                product.find_element(By.CLASS_NAME, "product-title").text for product in product_items
            ]
            product_prices = [
                float(product.find_element(By.CLASS_NAME, "prices")
                      .find_element(By.CLASS_NAME, "actual-price")
                      .text.replace("$", "").replace(",", "")) for product in product_items
            ]

            if option == "Price: Low to High":
                sorted_prices = sorted(product_prices)
                print("Sorted prices: ", sorted_prices)
                assert product_prices == sorted_prices, f"Products are not sorted by {option}."
            elif option == "Price: High to Low":
                sorted_prices = sorted(product_prices, reverse=True)
                print("Sorted prices (High to Low): ", sorted_prices)
                assert product_prices == sorted_prices, f"Products are not sorted by {option}."
            elif option == "Name: A to Z":
                assert product_names == sorted(product_names), f"Products are not sorted by {option}."
            elif option == "Name: Z to A":
                assert product_names == sorted(product_names, reverse=True), f"Products are not sorted by {option}."
            elif option == "Created on":
                logging.info("Sorting by 'Created on' is not implemented yet.")

    @allure.story("TC_SF_015: Validate the User can select how many products can be displayed in the Search Results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can select the number of products to be displayed per page from the 'Display' dropdown and ensures the correct number of products are displayed.")
    def test_display_number_of_products(self, driver, load_test_data):
        search_criteria = load_test_data["multiple_products_search"]["multiple_products"]
        display_options = ["3", "6", "9", "18"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_criteria)
        search_page.click(SearchPage.SEARCH_BUTTON)

        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(product_items) > 1, "Search did not return multiple products as expected."

        for option in display_options:
            search_page.select_dropdown_option(SearchPage.DISPLAY_DROPDOWN, option)

            time.sleep(3)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
            )

            product_items = driver.find_elements(By.CLASS_NAME, "product-item")
            assert len(product_items) <= int(
                option), f"Expected up to {option} products, but found {len(product_items)}."

    @allure.story("TC_SF_016: Validate 'Search' textbox field and the search button are displayed on all pages of the Application")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the 'Search' textbox field and the search button with 'Search' icon are displayed on all pages of the application.")
    def test_search_box_displayed_on_all_pages(self, driver, load_test_data):
        pages_to_test = [
            "/computers", "/electronics", "/apparel", "/digital-downloads",
            "/books", "/jewelry", "/gift-cards", "/desktops", "/notebooks",
            "/software", "/camera-photo", "/cell-phones", "/others",
            "/shoes", "/clothing", "/accessories"
        ]

        search_page = SearchPage(driver)
        search_page.open_url()

        for page in pages_to_test:
            driver.get(f"{driver.current_url}{page}")

            search_box = driver.find_element(By.ID, "small-searchterms")
            search_button = driver.find_element(By.XPATH, "//button[@class='button-1 search-box-button']")

            assert search_box.is_displayed(), f"Search textbox is not displayed on {page}."
            assert search_button.is_displayed(), f"Search button is not displayed on {page}."

    @allure.story("TC_SF_017: Validate navigating to Search page from the Sitemap page")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can navigate to the 'Search' page from the 'Sitemap' page by clicking on the 'Search' link.")
    def test_navigate_to_search_from_sitemap(self, driver):
        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.scroll_to_footer()

        sitemap_link = driver.find_element(By.LINK_TEXT, "Sitemap")
        sitemap_link.click()

        search_link = driver.find_element(By.LINK_TEXT, "Search")
        search_link.click()

        current_url = driver.current_url
        assert "search" in current_url, f"User was not navigated to the 'Search' page. Current URL: {current_url}"
        logging.info(f"User successfully navigated to the Search page. Current URL: {current_url}")

    @allure.story("TC_SF_018: Validate the use of all the options of Search functionality using the Keyboard keys")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can perform a search operation and select options on the Search page using only the Tab and Enter keys.")
    def test_search_using_keyboard_keys(self, driver, load_test_data):
        search_data_valid = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_field = driver.find_element(*SearchPage.SEARCH_FIELD)
        search_field.send_keys(search_data_valid)

        search_field.send_keys(Keys.TAB)
        search_field.send_keys(Keys.ENTER)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in the search results."

        assert any(search_data_valid in result.text for result in search_results), \
            f"The product '{search_data_valid}' is not found in the search results."

    @allure.story("TC_SF_019: Validate Page Heading, Page URL and Page Title of the 'Search' page")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the Page Heading, Page URL, and Page Title of the 'Search' page are correctly displayed after performing a product search.")
    def test_search_page_heading_url_and_title(self, driver, load_test_data):
        search_data_valid = load_test_data["product_search"]["valid_product"]

        search_page = SearchPage(driver)
        search_page.open_url()

        search_page.enter_text(SearchPage.SEARCH_FIELD, search_data_valid)
        search_page.click(SearchPage.SEARCH_BUTTON)

        page_heading = driver.find_element(By.CSS_SELECTOR, ".page-title h1").text
        assert page_heading == "Search", f"Expected page heading 'Search', but got '{page_heading}'."

        page_url = driver.current_url
        assert "search" in page_url, f"Expected URL to contain 'search', but got '{page_url}'."

        page_title = driver.title
        assert "Search" in page_title, f"Expected page title to contain 'Search', but got '{page_title}'."

    @allure.story("TC_SF_020: Validate the Search functionality in all the supported environments")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Cross-Browser")
    @allure.description(
        "This test validates that the search functionality works correctly in all the supported environments including different browsers, operating systems, and devices.")
    def test_search_functionality_on_supported_environments(self, driver, load_test_data):
        pytest.skip()

