#!/usr/bin/env python3
"""Format the issue comment that links the draft pull request."""

from __future__ import annotations

import os

from parse_sections import (
    changed_files_from_head,
    fallback,
    parse_sections,
    read_text,
    write_text,
)


def main() -> None:
    pr_url = os.environ.get("PR_URL", "").strip()
    output_path = os.environ.get("PR_COMMENT_PATH", "/tmp/pr-comment.md")

    resolve_text = read_text("/tmp/resolve-result.txt")
    triage_text = read_text("/tmp/triage-result.txt")
    resolve_sections = parse_sections(resolve_text)
    triage_sections = parse_sections(triage_text)

    changed_files = changed_files_from_head()

    summary = fallback(
        triage_sections.get("SUMMARY") or resolve_sections.get("PROBLEM"),
        "A valid issue was identified and a solution has been implemented.",
    )
    root_cause = fallback(
        resolve_sections.get("ROOT_CAUSE") or triage_sections.get("ROOT_CAUSE"),
        "See the Pull Request for the root cause analysis.",
    )
    resolution = fallback(
        resolve_sections.get("CHANGES_MADE"),
        "A solution has been implemented in a draft Pull Request.",
    )
    tests_executed = fallback(
        resolve_sections.get("TESTS_EXECUTED"),
        "See the Pull Request for test details.",
    )
    test_results = fallback(resolve_sections.get("TEST_RESULTS"), "")
    tests = tests_executed if not test_results else tests_executed + "\n\n" + test_results
    files = fallback(
        changed_files or resolve_sections.get("FILES_CHANGED"),
        "See the Pull Request diff.",
    )

    comment = "\n".join(
        [
            "## 🤖 T3Planet AI Bot",
            "",
            "### 🔍 Issue Analysis",
            "",
            "**Classification:** ✅ `VALID_ISSUE`",
            "",
            "### 📋 Summary",
            "",
            summary,
            "",
            "### 🔎 Root Cause",
            "",
            root_cause,
            "",
            "### 🛠️ Resolution",
            "",
            resolution,
            "",
            "### 🧪 Tests",
            "",
            tests,
            "",
            "### 📁 Files Changed",
            "",
            "```",
            files,
            "```",
            "",
            "### 🚀 Draft Pull Request",
            "",
            pr_url,
            "",
            "---",
            "",
            "The original Issue title and description were not modified.",
        ]
    )

    write_text(output_path, comment)


if __name__ == "__main__":
    main()
