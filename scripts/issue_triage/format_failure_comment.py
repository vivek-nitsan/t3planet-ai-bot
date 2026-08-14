#!/usr/bin/env python3
"""Format a short issue comment when the Cursor workflow fails."""

from __future__ import annotations

import os
from pathlib import Path

from parse_sections import read_text, write_text

TAIL_LINES = 80


def tail_text(path: str, lines: int = TAIL_LINES) -> str:
    text = read_text(path)
    if not text:
        return ""

    parts = text.splitlines()
    clipped = parts[-lines:]
    body = "\n".join(clipped).strip()

    if len(parts) > lines:
        return f"... truncated to last {lines} lines ...\n\n{body}"

    return body


def detect_stage() -> str:
    stage = (os.environ.get("CURSOR_STAGE") or "").strip()
    if stage:
        return stage

    return read_text("/tmp/cursor-stage.txt") or "unknown"


def detect_exit_code() -> str:
    code = (os.environ.get("CURSOR_EXIT_CODE") or "").strip()
    if code:
        return code

    return read_text("/tmp/cursor-exit-code.txt") or "unknown"


def main() -> None:
    output_path = os.environ.get("FAILURE_COMMENT_PATH", "/tmp/failure-comment.md")
    stage = detect_stage()
    exit_code = detect_exit_code()

    resolve_excerpt = tail_text("/tmp/resolve-result.txt")
    triage_excerpt = tail_text("/tmp/triage-result.txt")

    if stage == "resolve" or resolve_excerpt:
        excerpt = resolve_excerpt or triage_excerpt
        headline = "The automated implementation step failed."
    elif stage == "triage":
        excerpt = triage_excerpt
        headline = "The automated triage step failed."
    else:
        excerpt = resolve_excerpt or triage_excerpt
        headline = "The automated issue workflow failed."

    details = excerpt or "No Cursor output was captured."

    comment = "\n".join(
        [
            "## 🤖 T3Planet AI Bot",
            "",
            "### ⚠️ Automation Failed",
            "",
            headline,
            "",
            f"**Stage:** `{stage}`",
            "",
            f"**Exit code:** `{exit_code}`",
            "",
            "### 📋 Details",
            "",
            "```",
            details,
            "```",
            "",
            "No Pull Request was created. A maintainer can re-run the workflow after checking the failure.",
        ]
    )

    write_text(output_path, comment)
    print(f"Wrote failure comment to {Path(output_path)}")


if __name__ == "__main__":
    main()
