# <img src="assets/bot-icon.png" alt="T3Planet AI Bot" width="48" height="48" align="left" /> T3Planet AI Bot

<br clear="all" />

T3Planet AI Bot reviews GitHub Issues, classifies them, asks for missing information when needed, and creates a draft pull request when a code fix is required.

## Mandatory repository settings

Do these in **every** repository that uses the bot.

### 1. Actions permissions

Go to:

**Settings → Actions → General**

Under **Workflow permissions**:

- Select **Read and write permissions**
- Enable **Allow GitHub Actions to create and approve pull requests**

The workflow needs these because it creates branches, comments on issues, adds labels, pushes code, and creates draft PRs.

See GitHub docs: [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-default-github_token-permissions).

### 2. Repository secret

Go to:

**Settings → Secrets and variables → Actions**

Add:

| Name | Value |
|------|--------|
| `CURSOR_API_KEY` | Cursor API key from the [Cursor dashboard](https://cursor.com/dashboard/api) |

### 3. Workflow file

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
    uses: vivek-nitsan/t3planet-ai-bot/.github/workflows/issue-resolver.yml@main
    secrets:
      CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
    with:
      bot_ref: main
      base_branch: main
```

Example: [`examples/caller-workflow.yml`](examples/caller-workflow.yml)

## Optional

- Add a local `AGENTS.md` in your repository if you want project-specific rules. The bot always uses its default [`AGENTS.md`](AGENTS.md), then applies your local file if present.
- Change `base_branch` if your default branch is not `main`

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `bot_ref` | `main` | Branch/ref of this repo used to load scripts |
| `base_branch` | `main` | Default branch of the calling repository |

## License

MIT
