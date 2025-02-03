#!/bin/bash

# Run pytest and generate Allure results
pytest --alluredir=allure-results

echo "[Info] Allure results generated successfully!"

echo "[Info] Generating Allure report..."
# Generate the Allure report
allure generate allure-results -o allure-report --clean
echo "[Info] Allure report generated successfully!"

# Open the Allure report
allure open allure-report
