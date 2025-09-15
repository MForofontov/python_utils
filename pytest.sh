#!/bin/bash

# Default directories
DEFAULT_TEST_DIR="pytest/unit"
DEFAULT_ALLURE_RESULTS_DIR="pytest_run_tests/allure-results"
DEFAULT_ALLURE_REPORT_DIR="pytest_run_tests/allure-report"

# Allow overriding default directories via command-line arguments
TEST_DIR=${1:-$DEFAULT_TEST_DIR}
ALLURE_RESULTS_DIR=${2:-$DEFAULT_ALLURE_RESULTS_DIR}
ALLURE_REPORT_DIR=${3:-$DEFAULT_ALLURE_REPORT_DIR}
GENERATE_ALLURE=${4:-true}  # New option to control Allure report generation
RUN_PARALLEL=${5:-false}    # Option to run tests in parallel with pytest-xdist
EXTRA_ARGS=${6:-}           # Extra pytest arguments

# Function to print messages with timestamps
log_with_time() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_with_time "[Info] Running tests in: $TEST_DIR"

# Build pytest command with optional parallel execution and extra args
PYTEST_CMD="python -m pytest \"$TEST_DIR\""

# Add parallel execution if enabled
if [ "$RUN_PARALLEL" = "true" ]; then
    log_with_time "[Info] Running tests in parallel mode (-n auto)"
    PYTEST_CMD="$PYTEST_CMD -n auto"
fi

# Add extra arguments if provided
if [ -n "$EXTRA_ARGS" ]; then
    log_with_time "[Info] Using extra pytest arguments: $EXTRA_ARGS"
    PYTEST_CMD="$PYTEST_CMD $EXTRA_ARGS"
fi

if [ "$GENERATE_ALLURE" = "true" ]; then
    log_with_time "[Info] Storing Allure results in: $ALLURE_RESULTS_DIR"
    log_with_time "[Info] Generating Allure report in: $ALLURE_REPORT_DIR"

    # Run pytest with Allure results
    eval "$PYTEST_CMD --alluredir=\"$ALLURE_RESULTS_DIR\""

    log_with_time "[Info] Allure results generated successfully in $ALLURE_RESULTS_DIR!"

    if command -v allure >/dev/null 2>&1; then
        log_with_time "[Info] Generating Allure report..."
        # Generate the Allure report in the specified directory
        allure generate "$ALLURE_RESULTS_DIR" -o "$ALLURE_REPORT_DIR" --clean
        log_with_time "[Info] Allure report generated successfully in $ALLURE_REPORT_DIR!"

        # Only open report if not in CI environment
        if [ -z "$CI" ]; then
            allure open "$ALLURE_REPORT_DIR"
        else
            log_with_time "[Info] Skipping report opening in CI environment"
        fi
    else
        log_with_time "[Warn] Allure CLI not found. Skipping report generation."
    fi
else
    log_with_time "[Info] Skipping Allure report generation"
    # Run pytest without Allure
    eval "$PYTEST_CMD"
fi
