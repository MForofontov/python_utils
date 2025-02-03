#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run pytest and generate Allure results
pytest --alluredir=allure-results

# Generate the Allure report
allure generate allure-results -o allure-report --clean

# Open the Allure report
allure open allure-report