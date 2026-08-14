#!/usr/bin/env python3
"""Build the Stage 2 resolve prompt for cursor-agent."""

from __future__ import annotations

import os
from pathlib import Path

from parse_sections import format_comments, load_comments, read_text, write_text


def main() -> None:
    issue_number = os.environ["ISSUE_NUMBER"]
    issue_title = os.environ["ISSUE_TITLE"]
    issue_body = os.environ.get("ISSUE_BODY") or ""
    repository = os.environ.get("GITHUB_REPOSITORY") or "unknown"
    output_path = os.environ.get("RESOLVE_PROMPT_PATH", "/tmp/resolve-prompt.txt")
    triage_path = os.environ.get("TRIAGE_RESULT_PATH", "/tmp/triage-result.txt")

    comments_text = format_comments(
        load_comments(),
        "No comments have been added.",
    )
    triage_text = read_text(triage_path) or "No Stage 1 triage analysis was available."

    prompt = f"""
You are the coding agent responsible for resolving:

GitHub Issue #{issue_number}

Repository:
{repository}

Issue title:
{issue_title}

Original Issue description:
{issue_body}

Issue comments:
{comments_text}

============================================================
STAGE 1 TRIAGE ANALYSIS
============================================================

Reuse this analysis. Re-inspect the repository before changing code.

{triage_text}

============================================================
IMPORTANT
============================================================

FIRST read AGENTS.md.

Follow ALL applicable instructions from AGENTS.md.

You are already working on:

ai/fix-issue-{issue_number}

NEVER switch to main.

NEVER create another branch.

DO NOT:
- modify main
- commit changes
- push changes
- create a Pull Request
- modify the GitHub Issue
- modify Issue comments

GitHub Actions handles Git operations and PR creation.

============================================================
RESOLVE THE ISSUE
============================================================

1. Inspect the repository.
2. Understand the existing architecture.
3. Review the original issue and all relevant comments.
4. Identify the actual root cause.
5. Implement the smallest correct solution.
6. Follow existing coding style.
7. Do not make unrelated changes.
8. Add or update tests when appropriate.
9. Run the appropriate tests.
10. If tests fail because of your changes, investigate and fix them.
11. Run the relevant tests again.
12. Review the final git diff.
13. Leave the workspace clean: delete any temporary, junk, or
    unrelated files you created. Do not leave files that should
    not stay in git (.DS_Store, __pycache__, logs, .env, keys).

============================================================
IMPORTANT
============================================================

Do not blindly trust the issue description.

Verify that the reported problem is actually a defect by
inspecting the repository.

If the issue is no longer a real issue because of information
provided in the comments, do not make unrelated changes.

============================================================
TEST REQUIREMENT
============================================================

You MUST run the appropriate tests for the changes.

Do not claim that tests passed unless you actually ran them.

Report the exact test commands that were executed and their
results.

If no automated test is available or appropriate, explain why.

============================================================
FINAL REPORT
============================================================

Return exactly:

PROBLEM:
<problem>

ROOT_CAUSE:
<root cause>

FILES_CHANGED:
<files>

CHANGES_MADE:
<changes>

TESTS_EXECUTED:
<exact test commands>

TEST_RESULTS:
<test results>

IMPORTANT:

Do not report tests as passed unless they were actually executed.
"""

    write_text(output_path, prompt)
    print(f"Wrote resolve prompt to {Path(output_path)}")


if __name__ == "__main__":
    main()
