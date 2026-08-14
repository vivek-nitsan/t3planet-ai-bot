# AI Issue Resolver Rules

## General

- Never modify `main` directly.
- Always work only on the existing issue branch (`ai/fix-issue-<number>`).
- Keep changes minimal and scoped to the reported issue.
- Do not make unrelated changes or refactoring.
- Follow the existing project architecture and coding style.
- Do not modify this file (`AGENTS.md`) unless the issue explicitly requires it.
- Do not modify `.github/workflows/` or `.github/scripts/` unless the issue explicitly requires it.

## Issue Triage

Before changing code:

1. Read the complete GitHub Issue and relevant comments.
2. Read `AGENTS.md`.
3. Inspect the relevant repository code.
4. Determine whether the reported behavior is actually incorrect.
5. Do not guess when information is missing.

## Classification

Every issue must be classified as exactly one of:

### VALID_ISSUE

A real bug, defect, regression, or valid development request requiring a code change.

### NOT_AN_ISSUE

The current behavior is correct, or the request is a question, support request, or documentation request.

Do not modify code.

### NEEDS_INFORMATION

The issue may be valid, but there is not enough information to safely investigate or implement a fix.

Do not modify code.

## VALID_ISSUE

When the issue is valid:

1. Identify the root cause.
2. Implement the smallest correct solution.
3. Follow the existing architecture and coding style.
4. Add or update tests when appropriate.
5. Run relevant tests.
6. Fix failures caused by your changes.
7. Review the final diff.
8. Leave the workspace clean (see Workspace cleanliness).

## Git and GitHub Actions

GitHub Actions owns all git and GitHub operations.

- Never run `git commit`, `git push`, `git checkout`, or branch creation.
- Never run `gh` (issues, PRs, comments, labels).
- Never merge a Pull Request.
- Never modify the GitHub Issue title, description, labels, or comments.
- Never switch to `main`.

## Workspace cleanliness

Do not leave files that should not stay in git:

- Do not create or keep `.DS_Store`, `__pycache__/`, `*.pyc`, `*.log`, `tmp/`, or editor junk.
- Do not create or modify `.env`, credentials, keys, or secrets files.
- Do not add unrelated new files, temporary scratch files, or debug dumps.
- Do not change `.gitignore` unless required by the issue.
- Before finishing, remove any accidental temporary files you created.
- Only leave intentional source/test changes needed to fix the issue.

## Pull Request

The PR body (written by GitHub Actions from your report) must support:

- Problem
- Root cause
- Files changed
- Changes made
- Tests executed
- Test results

Return those sections in your final report. Do not claim tests passed unless you actually ran them.

## Issue

Never modify the original GitHub Issue title or description.

Only GitHub Actions may add comments when communication with the reporter is required.
