# Subscription authentication and continuous operation

This setup uses the official Codex CLI and official Claude Code CLI. Model requests use each owner's existing subscription. The server rental is still a separate cost. No API billing or paid usage top-up is enabled by this design.

## Account ownership

Assume the three Codex accounts belong to three authorized owners and the Claude account is used by its owner. Each owner signs into a separate Linux user on the rented server. If one person owns multiple accounts, confirm applicable account rules; separate directories do not make limit circumvention permissible.

Do not collect teammates' passwords, copy their tokens into a common pool, or retry a rate-limited owner's task through another login. Other owners' independent work may continue in their own lanes. The scheduler operates jobs; it does not combine accounts into one entitlement.

Use a trusted persistent server. Separate owner homes, Git credentials, CLI state, working clones, and task logs. Do not mount owner homes in bot-build or match containers. Keep host administration separate from unattended bot-development access.

## Codex: repeat once for each owner

The owner SSHs into their assigned Linux user and installs the official CLI using the current official installation instructions. Check its version and help before configuring the worker.

```bash
codex --version
codex login --device-auth
```

Complete the displayed sign-in in the owner's browser. Device-code login may need enabling in ChatGPT security/workspace settings. This leaves the CLI authenticated on the server; the laptop is not part of subsequent model requests. See [official authentication documentation](https://learn.chatgpt.com/docs/auth).

If device login is unavailable, the documented alternative is SSH forwarding for the browser callback, normally port 1455. Start `ssh -L 1455:localhost:1455 <owner>@<server>` from that owner's laptop, then run `codex login` remotely and follow the current CLI instructions. Do not forward the same local port for three simultaneous logins.

Keep the CLI's native credential directory persistent and owner-readable only. Prefer a fresh server login over cloning one live auth cache across machines. Let Codex perform its own refresh and retain the updated state. Do not overwrite refreshed credentials from an old seed on each restart. OpenAI documents account-auth use on trusted private automation and the hazards of concurrent use of copied caches: [CI/CD authentication guidance](https://learn.chatgpt.com/docs/auth/ci-cd-auth).

A bounded worker command, after the arena has created the task and schema, can take this form:

```bash
timeout --signal=TERM --kill-after=30s 20m \
  codex exec --sandbox workspace-write --json \
  --output-schema schemas/worker-result.schema.json \
  -o .agent/final.json \
  'Perform exactly one bot_worker task from .agent/task.json. Follow AGENTS.md and return the required structured result.'
```

The supervisor captures stdout/stderr privately, checks exit status, and validates the final file. Current docs say `--full-auto` is no longer supported; do not use an old tutorial's command. Preserve configured approval rules. If an allowed build wrapper cannot run under the approved sandbox, return a permission blocker and repair the wrapper/configuration deliberately; do not disable the sandbox automatically. [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)

Use subscription authentication only for these lanes. Keep API-key and external-provider settings out of their execution environment and verify the active auth method without printing token values. A successful login does not establish remaining quota.

## Claude Code: the Max owner's lane

Install the unmodified official Claude Code CLI, check its version, run `claude`, and select the owner's subscription login. Verify the account and billing mode in `/status`.

For a headless script-oriented setup, the official documentation also provides:

```bash
claude setup-token
```

The owner completes the official browser authorization. The command outputs a long-lived subscription token. Store it privately for that owner's worker as `CLAUDE_CODE_OAUTH_TOKEN`, using an owner-restricted credential mechanism. Never paste it into a prompt, repository, shared environment file, issue, or log. The documented token lifetime is one year, but revocation and account access changes can still require renewal. [Authentication](https://code.claude.com/docs/en/authentication)

Do not pass `--bare` in the subscription worker: the current headless documentation says that mode does not read subscription OAuth credentials. Use the official CLI directly; do not extract tokens for a custom inference proxy or generic model client. [Headless mode](https://code.claude.com/docs/en/headless) · [Credential-use guidance](https://code.claude.com/docs/en/legal-and-compliance)

An illustrative bounded invocation is:

```bash
timeout --signal=TERM --kill-after=30s 20m \
  claude -p --output-format json --max-turns 30 \
  --permission-mode acceptEdits --permission-prompts none \
  --allowedTools 'Read,Edit,Write,Glob,Grep,Bash(/usr/local/bin/bot-check *)' \
  'Perform exactly one bot_worker task from .agent/task.json. Follow AGENTS.md and return the required structured result.'
```

The `bot-check` executable is a trusted project wrapper to implement, not a preinstalled Claude tool. It must validate bot identity and run code only inside the approved build/match isolation. Check the installed CLI supports these flags; `--permission-prompts` requires v2.1.259 or newer. The supervisor can also pass the schema content through the CLI's documented `--json-schema` argument using a subprocess argument array. Validate the structured result; do not treat all JSON output as a successful task. [CLI reference](https://code.claude.com/docs/en/cli-reference)

Make sure `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, cloud-provider overrides, or `apiKeyHelper` are not silently selecting another billing path. Do not enable usage credits or Console fallback. Claude's plan limits are shared with other usage on the account; inspect the owner's status rather than assuming Max means unlimited. [Pro/Max usage](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)

The included CLAUDE.md imports AGENTS.md for compatibility. Current Claude Code can also load AGENTS.md directly under documented conditions; the explicit import avoids depending on a particular directory/configuration combination. [Project instructions](https://code.claude.com/docs/en/memory)

## What 24/7 means operationally

| Situation | Required behavior |
|---|---|
| Laptop disconnects | Server services keep running |
| One account reaches its limit | Save its state; wait for its actual reset; independent lanes continue |
| All accounts reach limits | Finish useful queued evaluations or bounded parameter sweeps; wait without LLM polling |
| Login expires or refresh fails | Mark AUTH_REQUIRED; preserve work; owner signs in again |
| CLI crashes or task times out | Save partial changes; launch an explicit recovery task later |
| GitHub is unavailable | Keep evaluated artifacts and pending source publication; retry with backoff |
| Server restarts | systemd restarts supervisors; reconcile persistent state before issuing new work |
| Official platform is unavailable | Private arena continues; external tasks pause |

There is no promise that three unspecified Codex plans plus one unspecified Max tier can sustain four simultaneous reasoning sessions forever. OpenAI and Anthropic expose changing plan-dependent limits. Check each owner's actual plan, available model, usage dashboard, and reset times. [Codex usage](https://learn.chatgpt.com/docs/pricing)

Start on an owner-selected standard-speed model, with moderate effort for ordinary edits and deeper effort only for difficult diagnosis. Keep model selection in per-owner configuration rather than hard-coding a model identifier in these prompts. Tune task frequency from actual outcomes and remaining allocation. Log token usage when reported, but do not convert token counts into invented remaining subscription quota.

## Minimum operating routine

Run the arena and worker supervisors under systemd, not an SSH shell or tmux alone. Each unit needs a real Linux User, a pinned WorkingDirectory and executable, persistent state, restart backoff, and process-group cleanup. Account owners need not leave a terminal open.

Once per day, inspect a concise status report for auth/quota waits, stale feedback, failed matches, and disk pressure. Keep code in the private repo and take consistent database/artifact backups. Updates to CLIs, SDKs, toolchains, or maps should be pinned and smoke-tested before replacing the running version.

Competition login is separate from Codex/Claude login. The inspected `cambc login` help says its platform session lasts seven days. Only the publisher needs that credential. Its expiry must not stop local simulation or bot improvement; unattended renewal behavior was not verified.
