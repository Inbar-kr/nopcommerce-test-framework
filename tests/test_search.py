import time
import pytest
import json
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys

from pages.login_page import LoginPage
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
        search_page = SearchPage(driver)

        search_page.search_valid_product(load_test_data)

        search_page.logger.info("User successfully searching for an existing product.")

    @allure.story("TC_SF_002: Validate searching with a non-existing Product Name")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates that searching for a non-existing product displays an appropriate message.")
    def test_invalid_product_search(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_invalid_product(load_test_data)

        search_page.logger.info("Searching for a non-existing product displays an appropriate message")

    @allure.story("TC_SF_003: Validate searching without providing any Product Name")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates that searching without entering a product name displays an appropriate popup message.")
    def test_empty_product_search(self, driver):
        search_page = SearchPage(driver)

        search_page.empty_search()

        search_page.logger.info("Searching without entering a product displays an appropriate message")

    @allure.story("TC_SF_004: Validate searching for a product after login to the Application")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for an existing product after logging in displays the correct product in the search results.")
    def test_search_product_after_login(self, driver, load_test_data):
        login_page = LoginPage(driver)
        login_page.login_user(driver, load_test_data)

        search_page = SearchPage(driver)
        search_page.search_valid_product(load_test_data)

        search_page.logger.info("User successfully searching for an existing product after logging in.")

    @allure.story("TC_SF_005: Validate searching by providing a search criteria which results in multiple products")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching with a criteria that returns multiple products displays more than one product in the search results.")
    def test_search_multiple_products(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_multiple_products(load_test_data)

        search_page.logger.info("User successfully searching for multiple existing products.")

    @allure.story("TC_SF_006: Validate all the fields in the Search functionality and Search page have placeholders")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all fields on the Search page have the correct placeholder text.")
    def test_search_field_placeholders(self, driver):
        search_page = SearchPage(driver)

        search_page.validate_placeholders(driver)

        search_page.logger.info("All search fields have the correct placeholders.")

    @allure.story("TC_SF_007: Validate searching using 'Search keyword' field")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching using the 'Search keyword' field works and displays the correct product in the search results.")
    def test_search_using_keyword_field(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_using_search_keyboard_field(driver, load_test_data)

        search_page.logger.info("Search successful using 'Search keyword' field.")

    @allure.story("TC_SF_008: Validate Search using the text from the product description")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for a product using text from its description returns the correct product in the search results.")
    def test_search_using_product_description(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_using_product_description(driver, load_test_data)

        search_page.logger.info("Search successful using product description.")

    @allure.story("TC_SF_009: Validate Search by selecting the category of product")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that searching for a product by selecting the correct or incorrect category returns the expected results.")
    def test_search_by_category(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_by_category(load_test_data)

        search_page.logger.info("Search successful by selecting the category of product.")

    @allure.story("TC_SF_010: Validate Search by selecting to search in subcategories")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that searching with the 'Automatically search subcategories' option enabled returns the expected results.")
    def test_search_in_subcategories(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_in_subcategories(load_test_data)

        search_page.logger.info("Search successful by selecting to search in subcategories.")

    @allure.story("TC_SF_011: Validate List and Grid views when only one Product and multiple Products is displayed in the search results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the List and Grid views for a single product displayed in the search results and verifies navigation to the Product Display Page.")
    def test_list_and_grid_views_single_product(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.list_and_grid_views(driver, load_test_data)

        search_page.logger.info("Search successful by viewing List and Grid views when only one Product and multiple Products is displayed.")

    @allure.story("TC_SF_012: Validate page navigation when multiple products are displayed.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("Regression")
    @allure.description("This test validates page navigation for search results when multiple products are displayed.")
    def test_pages_views_products(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.pages_views_products(driver, load_test_data)

        search_page.logger.info("Search successful by navigation when multiple products are displayed.")

    @allure.story("TC_SF_013: Validate adding to Product Compare Page from Search Results page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that products can be added to the compare list from the search results page and verifies that the user is navigated to the Product Compare Page.")
    def test_add_to_compare_page_from_search_results(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.compare_products(driver, load_test_data)

        search_page.logger.info("Search successful by viewing that adding to Product Compare Page from Search Results page.")

    @allure.story("TC_SF_014: Validate User is able to sort the Products displayed in the Search Results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that products can be sorted according to the selected option from the 'Sort By' dropdown on the Search Results page.")
    def test_sort_products_in_search_results(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.sort_products(driver, load_test_data)

        search_page.logger.info("Search successful by viewing that the products can be sorted according to the selected option.")

    @allure.story("TC_SF_015: Validate the User can select how many products can be displayed in the Search Results")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can select the number of products to be displayed per page from the 'Display' dropdown and ensures the correct number of products are displayed.")
    def test_display_number_of_products(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.display_number_of_products(driver, load_test_data)

        search_page.logger.info("Search successful by viewing that the user can select the number of products.")

    @allure.story("TC_SF_016: Validate 'Search' textbox field and the search button are displayed on all pages of the Application")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the 'Search' textbox field and the search button with 'Search' icon are displayed on all pages of the application.")
    def test_search_box_displayed_on_all_pages(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_box_displayed_on_all_pages(driver)

        search_page.logger.info("Search successful by viewing that the 'Search' textbox field and the search button are displayed on all pages.")

    @allure.story("TC_SF_017: Validate navigating to Search page from the Sitemap page")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can navigate to the 'Search' page from the 'Sitemap' page by clicking on the 'Search' link.")
    def test_navigate_to_search_from_sitemap(self, driver):
        search_page = SearchPage(driver)

        search_page.navigate_from_sitemap(driver)

        search_page.logger.info("Validate navigating to Search page from the Sitemap page.")

    @allure.story("TC_SF_018: Validate the use of all the options of Search functionality using the Keyboard keys")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can perform a search operation and select options on the Search page using only the Tab and Enter keys.")
    def test_search_using_keyboard_keys(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.search_using_keyboard_keys(driver, load_test_data)

        search_page.logger.info("Validate the use of all the options of Search functionality using the Keyboard keys.")

    @allure.story("TC_SF_019: Validate Page Heading, Page URL and Page Title of the 'Search' page")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the Page Heading, Page URL, and Page Title of the 'Search' page are correctly displayed after performing a product search.")
    def test_search_page_heading_url_and_title(self, driver, load_test_data):
        search_page = SearchPage(driver)

        search_page.heading_url_and_title(driver, load_test_data)

        search_page.logger.info("Validate Page Heading, Page URL and Page Title of the 'Search' page.")

    @allure.story("TC_SF_020: Validate the Search functionality in all the supported environments")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Cross-Browser")
    @allure.description(
        "This test validates that the search functionality works correctly in all the supported environments including different browsers, operating systems, and devices.")
    def test_search_functionality_on_supported_environments(self, driver, load_test_data):
        pytest.skip()

