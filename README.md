# <img src="assets/bot-icon.png" alt="T3Planet AI Bot" width="48" height="48" align="left" /> T3Planet AI Bot

<br clear="all" />

Public reusable GitHub Action workflow that triages GitHub Issues with Cursor and opens a draft PR when a code fix is needed.

Repository: https://github.com/vivek-nitsan/t3planet-ai-bot

## Features

- Classifies issues as `VALID_ISSUE`, `NOT_AN_ISSUE`, or `NEEDS_INFORMATION`
- Asks for missing details and re-runs when the reporter replies
- Implements fixes with Cursor CLI
- Opens a draft pull request with **solution source files only**

## Use in any repository

### 1. Add a repository secret

Create `CURSOR_API_KEY` in the target repo (Cursor dashboard → API keys).

### 2. Add a thin workflow

Create `.github/workflows/t3planet-ai-bot.yml`:

```yaml
name: T3Planet AI Bot

on:
  issues:
    types: [opened]
  issue_comment:
    types: [created]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  resolve:
    if: |
      github.event_name == 'issues' ||
      (
        github.event_name == 'issue_comment' &&
        !github.event.issue.pull_request &&
        github.event.comment.user.type != 'Bot' &&
        contains(github.event.issue.labels.*.name, 'needs-information')
      )
    uses: vivek-nitsan/t3planet-ai-bot/.github/workflows/issue-resolver.yml@v1
    secrets:
      CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
    with:
      bot_ref: v1
      base_branch: main
```

See [`examples/caller-workflow.yml`](examples/caller-workflow.yml).

### 3. Rules (`AGENTS.md`)

You do **not** need an `AGENTS.md` in every project.

- Canonical rules live in this bot: [`AGENTS.md`](AGENTS.md)
- Optional: add a local `AGENTS.md` only for project-specific extras
- The bot always loads bot rules from `/tmp/t3planet-ai-bot/AGENTS.md` during the run

## Permitted files in automated PRs

Only product/solution source is committed and pushed.

### Allowed (examples)

| Area | Examples |
|------|----------|
| PHP classes | `Classes/**/*.php` |
| TYPO3 configuration | `Configuration/**/*` |
| Extension templates/assets | `Resources/Private/**/*`, `Resources/Public/**/*` |
| Extension entrypoints | `ext_localconf.php`, `ext_tables.php`, `ext_emconf.php` |
| Metadata when required by the issue | `composer.json` |

### Not allowed (never pushed)

| Area | Examples |
|------|----------|
| Git meta | `.gitignore`, `.gitattributes` |
| Tests / smoke | `Tests/**`, `tests/**`, `*smoke*` |
| Docs / license / rules | `README.md`, `LICENSE`, `AGENTS.md`, most `Documentation/**` |
| CI / tooling | `.github/**`, `.cursor/**` |
| Secrets | `.env`, `*.key`, `*.pem` |
| Junk | `.DS_Store`, `__pycache__/`, `*.log`, `tmp/` |

If Cursor creates excluded files locally, the workflow skips them and does not push them.

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `bot_ref` | `v1` | Tag/ref of this repo used to load scripts |
| `base_branch` | `main` | Default branch of the calling repository |

## Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `CURSOR_API_KEY` | yes | Cursor API key for `cursor-agent` |

## Notes for public reuse

- This repository must stay **public** (or callers need access) so other repos can `uses:` it.
- Keep `bot_ref` aligned with the workflow ref (`@v1` → `bot_ref: v1`).
- Each calling repo needs its own `CURSOR_API_KEY` secret (or an org secret).

## License

MIT
