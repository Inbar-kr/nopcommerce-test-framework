# Selenium Test Suite for nopCommerce

## Project Overview

This project is an automated test suite for validating the functionality and performance of the nopCommerce platform.  
The test suite is built using Selenium WebDriver with Python (Pytest) and integrated into a CI/CD pipeline using GitHub Actions to ensure consistent and reliable test execution.  
It focuses on automating key functionalities like user registration, login, product search, and checkout operations.

## Features

* Automated functional tests for critical nopCommerce features.
* Cross-browser testing on Chrome, Firefox.
* CI/CD integration using GitHub Actions for automated test execution.
* Detailed reporting with Allure, including test logs and screenshots of failed tests.
* Parallel execution to reduce test execution time.

## Technologies Used

* Selenium WebDriver: Browser automation.
* Python (Pytest): Test framework for writing and managing test cases.
* GitHub Actions: For CI/CD pipeline setup and test automation.
* Allure: Reporting tool for generating detailed test execution reports.


## Setup and Installation

#### Pre-requisites
* Python 3.10 or above  
* Google Chrome, Mozilla Firefox  
* ChromeDriver, GeckoDriver  
* GitHub repository with Actions enabled

#### Installation Steps

1. Clone the repository:
 [git clone](https://github.com/Inbar-kr/nopcommerce-test-framework.git)
`cd test_automation_framework`

2. Install dependencies:
`pip install -r requirements.txt`
3. Set up your browser drivers (ChromeDriver, GeckoDriver).
4. Configure CI/CD pipeline:  
   GitHub Actions workflows are defined in `.github/workflows/ci-cd-pipeline.yml`.
5. Generate Allure reports:
`pytest --alluredir=reports/allure-results`
`allure serve reports/allure-results`

## How to Run Tests

#### Local Execution

1. Run all tests:
`pytest`
2. Run specific test markers:.

    Smoke Tests: pytest `-m smoke`
    Regression Tests: `pytest -m regression`

#### CI/CD Pipeline Execution
* Push or commit changes to the repository.  
* GitHub Actions automatically triggers the pipeline.  
* View the test execution results in the **Actions** tab on GitHub.
    ###### Note: Some tests may fail in CI/CD due to CAPTCHA behavior in headless mode. Tests run successfully in headed (local) mode without issues.

## Reporting
Allure Reports: Automatically generated in reports/allure-results. View reports with:
`allure serve reports/allure-results`

## Test Run Reports
[Test Run - nopCommerce Test Cases](https://test-management.browserstack.com/projects/343197/test-runs/TR-18/folder?public_token=53ad5e810e198d3e4c63f5b0de70c98864aa0fd4da895e961991beb58594e653147bdb52bbb8c21181fab065ca8920bb3bd4c9dbab2b2b4643019143cd2a5b35&public_token_id=3216)

###### Note: This project is a personal and educational portfolio project. It is not intended for redistribution or external use.