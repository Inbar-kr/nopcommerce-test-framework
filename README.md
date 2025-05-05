# Selenium CI/CD Test Suite for nopCommerce

## Project Overview

This project is an automated test suite for validating the functionality and performance of the nopCommerce platform. 
The test suite is built using Selenium WebDriver with Python (Pytest) and integrated into a CI/CD pipeline to ensure consistent and reliable test execution. 
It focuses on automating key functionalities like user registration, login, product search and checkout operations.

## Features

* Automated functional tests for critical nopCommerce features.
* Cross-browser testing on Chrome, Firefox, and Edge.
* CI/CD integration using GitLab CI for automated test execution.
* Detailed reporting with Allure for test logs, screenshots of failed tests.
* Parallel execution to reduce test execution time.

## Technologies Used

* Selenium WebDriver: Browser automation.
* Python (Pytest): Test framework for writing and managing test cases.
* GitLab CI: For CI/CD pipeline setup and execution.
* Allure: Reporting tool for generating detailed test execution reports.


## Setup and Installation

#### Pre-requisites
* Python 3.10 or above
* Google Chrome, Mozilla Firefox
* ChromeDriver, GeckoDriver
* GitLab CI configured on your system

#### Installation Steps

1. Clone the repository:
 [git clone](https://github.com/Inbar-kr/nopcommerce-test-framework.git)
`cd test_automation_framework`

2. Install dependencies:
`pip install -r requirements.txt`
3. Set up your browser drivers (ChromeDriver, GeckoDriver).
4. Configure the CI/CD pipeline:
For GitLab CI: Use the ci-cd-pipeline.yml file.
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
* Commit your changes to the repository.
* Trigger the pipeline in GitLab CI.
* View the test execution results in the CI/CD dashboard.

## Reporting
Allure Reports: Automatically generated in reports/allure-results. View reports with:
`allure serve reports/allure-results`

## Test Run Reports
1. [Test Run Summary](https://test-management.browserstack.com/projects/343197/reports/27682?public_token=c193e9f680fb7098065237a261b13b6be7ea8c8c09c18e5496255752e1e403dce359ed068f3c9421ce3ac29a4c7546818050a6a04ebb6824dada72e94a48a95b&public_token_id=1361)
2. [Test Run - nopCommerce Test Cases](https://test-management.browserstack.com/projects/343197/test-runs/TR-18?public_token=562d57b5dd3a7f3292cfe08ea247426569ef028817ba85e9790cc374460779d36453e2fe70088dc87e90396e83bb4288dd844dd24720f9d271c822b1bd26b273&public_token_id=1362)

###### Note: This project is a private repository created for personal and portfolio purposes. It is not intended for redistribution or external use.