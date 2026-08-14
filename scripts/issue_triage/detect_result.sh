#!/usr/bin/env bash
set -euo pipefail

RESULT_FILE="${1:-/tmp/triage-result.txt}"

if [ ! -s "$RESULT_FILE" ]; then
  echo "Cursor returned an empty response."
  echo "No Pull Request will be created."
  exit 1
fi

RESULT=$(
  grep -Eio \
    'RESULT:[[:space:]]*(VALID_ISSUE|NOT_AN_ISSUE|NEEDS_INFORMATION)' \
    "$RESULT_FILE" \
    | head -n 1 \
    | sed -E 's/.*RESULT:[[:space:]]*//' \
    | tr '[:lower:]' '[:upper:]' \
    | tr -d '\r' \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//'
) || true

if [ -z "$RESULT" ]; then
  if grep -Eiq '\bNOT_AN_ISSUE\b' "$RESULT_FILE"; then
    RESULT="NOT_AN_ISSUE"
  elif grep -Eiq '\bNEEDS_INFORMATION\b' "$RESULT_FILE"; then
    RESULT="NEEDS_INFORMATION"
  elif grep -Eiq '\bVALID_ISSUE\b' "$RESULT_FILE"; then
    RESULT="VALID_ISSUE"
  else
    RESULT="REVIEW_REQUIRED"
  fi
fi

echo "Detected classification: ${RESULT}"

if [ -n "${GITHUB_ENV:-}" ]; then
  echo "RESULT=${RESULT}" >> "$GITHUB_ENV"
fi
