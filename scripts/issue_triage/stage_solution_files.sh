#!/usr/bin/env bash
# Stage only solution source files for the automated PR.
# Excluded paths are left untracked / unstaged and are never pushed.
set -euo pipefail

is_excluded() {
  local path="$1"

  case "$path" in
    .gitignore|.gitattributes|AGENTS.md|README.md|LICENSE|LICENSE.md)
      return 0
      ;;
    .github|.github/*|.cursor|.cursor/*|_t3planet_ai_bot|_t3planet_ai_bot/*)
      return 0
      ;;
    Tests|Tests/*|*/Tests/*|tests|tests/*|*/tests/*)
      return 0
      ;;
    *smoke*|*Smoke*|*SMOKE*)
      return 0
      ;;
    .DS_Store|*/.DS_Store|__pycache__|__pycache__/*|*/__pycache__/*|*.pyc|*.log|tmp|tmp/*|temp|temp/*)
      return 0
      ;;
    .env|.env.*|*.key|*.pem|*credential*|node_modules|node_modules/*)
      return 0
      ;;
  esac

  return 1
}

is_dangerous() {
  local path="$1"

  case "$path" in
    .env|.env.*|*.key|*.pem|*credential*|node_modules|node_modules/*)
      return 0
      ;;
  esac

  return 1
}

# Remove junk so it does not linger
find . -name .DS_Store -type f -delete 2>/dev/null || true
find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -type f -delete 2>/dev/null || true

git reset >/dev/null 2>&1 || true

dangerous=""
skipped=""
staged=""

while IFS= read -r line; do
  [ -z "$line" ] && continue

  status="${line:0:2}"
  path="${line:3}"
  path="${path#\"}"
  path="${path%\"}"

  # Renames show as "old -> new"
  if [[ "$path" == *" -> "* ]]; then
    path="${path##* -> }"
  fi

  if is_dangerous "$path"; then
    dangerous="${dangerous}${path}"$'\n'
    continue
  fi

  if is_excluded "$path"; then
    skipped="${skipped}${path}"$'\n'
    # Discard tracked modifications to excluded files so they are not pushed
    if [ "$status" != "??" ] && [ "$status" != "A " ]; then
      git checkout -- "$path" 2>/dev/null || true
    fi
    continue
  fi

  git add -- "$path"
  staged="${staged}${path}"$'\n'
done < <(git status --porcelain)

if [ -n "$dangerous" ]; then
  printf '%s' "$dangerous" > /tmp/dangerous-files.txt
  echo "Dangerous files were produced and must not be committed:"
  printf '%s' "$dangerous"
  exit 2
fi

if [ -n "$skipped" ]; then
  echo "Skipping non-solution files (not pushed):"
  printf '%s' "$skipped"
fi

if [ -z "$(git diff --cached --name-only)" ]; then
  echo "No solution source files to commit."
  echo "has_solution_changes=false"
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "has_solution_changes=false" >> "$GITHUB_OUTPUT"
  fi
  exit 0
fi

echo "Staging solution files:"
git diff --cached --name-only
echo "has_solution_changes=true"
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "has_solution_changes=true" >> "$GITHUB_OUTPUT"
fi
