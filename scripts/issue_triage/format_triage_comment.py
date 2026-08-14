#!/usr/bin/env python3
"""Format the issue comment for a Stage 1 triage result."""

from __future__ import annotations

import os

from parse_sections import bullet_list, fallback, parse_sections, read_text, write_text


def main() -> None:
    result = os.environ.get("RESULT", "REVIEW_REQUIRED").strip()
    triage_path = os.environ.get("TRIAGE_RESULT_PATH", "/tmp/triage-result.txt")
    output_path = os.environ.get("ISSUE_COMMENT_PATH", "/tmp/issue-comment.md")

    triage_text = read_text(triage_path)
    sections = parse_sections(triage_text)

    summary = fallback(
        sections.get("SUMMARY"),
        triage_text or "No summary was returned.",
    )
    root_cause = fallback(
        sections.get("ROOT_CAUSE") or sections.get("ANALYSIS"),
        triage_text or "No root cause was returned.",
    )
    recommendation = fallback(
        sections.get("RECOMMENDATION"),
        "Please review the issue details.",
    )
    explanation = fallback(
        sections.get("ANALYSIS") or sections.get("ROOT_CAUSE") or sections.get("SUMMARY"),
        triage_text or "No explanation was returned.",
    )
    proposed_solution = fallback(
        sections.get("PROPOSED_SOLUTION") or sections.get("RECOMMENDATION"),
        "A solution will be implemented if a code change is required.",
    )
    required_information = fallback(
        sections.get("REQUIRED_INFORMATION"),
        "Please provide more information about the issue.",
    )

    if result == "NOT_AN_ISSUE":
        comment = "\n".join(
            [
                "## 🤖 T3Planet AI Bot",
                "",
                "### 🔍 Issue Analysis",
                "",
                "**Classification:** ❌ `NOT_AN_ISSUE`",
                "",
                "### ℹ️ Explanation",
                "",
                explanation,
                "",
                "### 📚 Recommendation",
                "",
                recommendation,
                "",
                "No code changes were made and no Pull Request was created.",
            ]
        )
    elif result == "NEEDS_INFORMATION":
        comment = "\n".join(
            [
                "## 🤖 T3Planet AI Bot",
                "",
                "### 🔍 Issue Analysis",
                "",
                "**Classification:** ❓ `NEEDS_INFORMATION`",
                "",
                "### ❓ Information Required",
                "",
                bullet_list(required_information),
                "",
                "Please provide the requested information in a new comment.",
                "",
                "I will re-check the issue when you provide the information.",
            ]
        )
    elif result == "VALID_ISSUE":
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
                "### 🛠️ Proposed Resolution",
                "",
                proposed_solution,
                "",
                "The issue has enough information to proceed with implementation.",
            ]
        )
    else:
        comment = "\n".join(
            [
                "## 🤖 T3Planet AI Bot",
                "",
                "### 🔍 Issue Analysis",
                "",
                "**Classification:** ⚠️ `REVIEW_REQUIRED`",
                "",
                "### ⚠️ Warning",
                "",
                "The automated classification could not be determined.",
                "",
                "### 📋 Analysis",
                "",
                triage_text or "No analysis was returned.",
                "",
                "No code changes or Pull Request were created.",
            ]
        )

    write_text(output_path, comment)


if __name__ == "__main__":
    main()
