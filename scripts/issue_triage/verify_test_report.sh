#!/usr/bin/env bash
set -euo pipefail

RESULT_FILE="${1:-/tmp/resolve-result.txt}"

echo "Checking Cursor test report..."

if [ ! -s "$RESULT_FILE" ]; then
  echo "ERROR: Cursor resolution report is empty."
  exit 1
fi

extract_section() {
  local heading="$1"

  awk -v heading="$heading" '
    {
      line = $0
    }
    tolower(line) ~ "^" tolower(heading) ":" {
      found = 1
      sub("^[^:]+:[[:space:]]*", "")
      if ($0 != "") print
      next
    }
    found && /^[A-Z_]+:/ { exit }
    found { print }
  ' "$RESULT_FILE"
}

if ! grep -Eiq '^TESTS_EXECUTED:' "$RESULT_FILE"; then
  echo "ERROR: Cursor did not provide TESTS_EXECUTED."
  exit 1
fi

if ! grep -Eiq '^TEST_RESULTS:' "$RESULT_FILE"; then
  echo "ERROR: Cursor did not provide TEST_RESULTS."
  exit 1
fi

TESTS_EXECUTED="$(extract_section "TESTS_EXECUTED")"
TEST_RESULTS="$(extract_section "TEST_RESULTS")"

if [ -z "$(printf '%s' "$TESTS_EXECUTED" | tr -d '[:space:]')" ]; then
  echo "ERROR: TESTS_EXECUTED is empty."
  exit 1
fi

if [ -z "$(printf '%s' "$TEST_RESULTS" | tr -d '[:space:]')" ]; then
  echo "ERROR: TEST_RESULTS is empty."
  exit 1
fi

if printf '%s\n' "$TEST_RESULTS" | awk '
  {
    line = tolower($0)
    gsub(/0[[:space:]]*(failed|failure|failures|error|errors)/, " ", line)
    gsub(/(failed|failure|failures|error|errors)[[:space:]]*:[[:space:]]*0/, " ", line)
    gsub(/no[[:space:]]+(failed|failure|failures|error|errors)/, " ", line)
    gsub(/without[[:space:]]+(failed|failure|failures|error|errors)/, " ", line)
    gsub(/not[[:space:]]+an[[:space:]]+error/, " ", line)
    if (line ~ /(failed|failure|failures|error|errors|not passed|unsuccessful)/) {
      found = 1
    }
  }
  END {
    exit found ? 0 : 1
  }
'; then
  echo ""
  echo "ERROR: Cursor reported test failures."
  echo "No Pull Request will be created."
  exit 1
fi

echo ""
echo "========== TEST REPORT =========="
echo "$TEST_RESULTS"
echo "================================="

echo "Test report accepted."
