# Selenium CI/CD Test Suite for nopCommerce

## Project Overview

This project is an automated test suite for validating the functionality and performance of the nopCommerce platform. 
The test suite is built using Selenium WebDriver with Python (Pytest) and integrated into a CI/CD pipeline to ensure consistent and reliable test execution. 
It focuses on automating key functionalities like user registration, login, product search and checkout operations.

## Features

* Automated functional tests for critical nopCommerce features.
* Cross-browser testing on Chrome, Firefox, and Edge.
* CI/CD integration using Jenkins/GitLab CI for automated test execution.
* Detailed reporting with Allure for test logs, screenshots of failed tests.
* Parallel execution to reduce test execution time.

## Technologies Used

* Selenium WebDriver: Browser automation.
* Python (Pytest): Test framework for writing and managing test cases.
* GitLab CI: For CI/CD pipeline setup and execution.
* Allure: Reporting tool for generating detailed test execution reports.


## Setup and Installation

#### Pre-requisites
* Python 3.12.2 or above
* Google Chrome, Mozilla Firefox
* ChromeDriver, GeckoDriver
* GitLab CI configured on your system

#### Installation Steps

1. Clone the repository:
git clone https://github.com/Inbar-kr/nopcommerce-test-framework.git
`cd test_automation_framework`

2. Install dependencies:
`pip install -r requirements.txt`
3. Set up your browser drivers (ChromeDriver, GeckoDriver, EdgeDriver).
4. Configure the CI/CD pipeline:
For GitLab CI: Use the ci-cd-pipeline.yml file.
5. Generate Allure reports:
`pytest --alluredir=reports/allure-results`
`allure serve reports/allure-results`

## How to Run Tests

#### Local Execution
Run all tests:
`pytest`

#### CI/CD Pipeline Execution
* Commit your changes to the repository.
* Trigger the pipeline in GitLab CI.
* View the test execution results in the CI/CD dashboard.

## Reporting
Allure Reports: Automatically generated in reports/allure-results. View reports with:
`allure serve reports/allure-results`


###### Note: This project is a private repository created for personal and portfolio purposes. It is not intended for redistribution or external use.