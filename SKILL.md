---
name: claude-delegate
description: Delegate a bounded coding, investigation, or review task to a local Claude Code CLI when the user requests Claude Code delegation. Codex defines the authority boundary, reviews the actual result, and independently verifies supported changes.
---

# Delegate to Claude Code

Use Claude Code as an external worker. Codex remains responsible for scope,
permissions, billing and capacity gates, integration, verification, and the
final answer.

## Boundaries

- Claude does not inherit the Codex conversation. Include every material
  instruction and constraint in its assignment.
- Treat existing changes as user-owned. Preserve unrelated work and never edit
  the same checkout while Claude is running.
- Never use a permission-bypass mode or silently widen tools, settings, scope,
  or authority after a denial.
- Do not commit, push, publish, deploy, install dependencies, access unrelated
  external systems, or remove user-owned files without explicit authorization.
- A worktree separates edits; it is not a security sandbox and does not include
  uncommitted changes unless they are deliberately transferred.
- Do not opt into separately billed models, modes, extended context, or extra
  usage without the user's informed authorization. Honor local model policies.
- Treat Claude's report as evidence to inspect, not proof of success.

## 1. Preflight

1. Confirm the repository or disposable workspace. Read applicable `AGENTS.md`,
   `CLAUDE.md`, and other repository instructions, then record `git status
   --short`, including untracked files.
2. Run `claude --version` and `claude --help`. Capture `claude auth status` as
   structured data, but emit only an allowlist of login state, auth method,
   provider, and subscription type. Never run it as a standalone captured
   command or put raw identity fields in the transcript. Read
   [references/cli-compatibility.md](references/cli-compatibility.md) and verify
   every security-relevant flag against the installed CLI before launch.
3. Establish the authorized authentication and billing profile:
   subscription, API, supported cloud provider, or unknown. Inspect only the
   presence of credential/provider environment variables; never print values.
   Stop if the active profile is ambiguous or differs from what the user
   authorized.
4. Capture relevant Claude and Codex capacity when available. Read
   [references/usage-monitoring.md](references/usage-monitoring.md) before
   interpreting or reporting usage. Unknown telemetry is not zero capacity.
5. Do not launch if an observed applicable limit is reached or if too little
   Codex capacity remains for independent review.

## 2. Define and route the assignment

Specify one objective, exact owned paths, prohibited actions, observable
acceptance criteria, exact authorized checks, working directory, retention of
artifacts, and a proportional turn limit. Choose a model and effort using
[references/model-routing.md](references/model-routing.md).

Owned paths are a prompt contract checked through the complete post-run diff;
restricted mode confines file tools to working directories but does not enforce
a per-file allowlist. Use a minimized disposable checkout or worktree when the
worker must not see or edit other files in the repository.

Honor explicit user choices. Do not silently substitute a model or assume an
effort level was applied. Allow at most one reasoning escalation, and only when
review shows reasoning capability—not permissions, authentication, capacity,
environment, or an ordinary defect—was the likely limitation.

## 3. Launch within the boundary

Read [references/assignment-and-permissions.md](references/assignment-and-permissions.md)
before every launch. Load [references/report-schema.json](references/report-schema.json)
and pass it with `--json-schema`.

Use noninteractive JSON output, deterministic unattended denial, restricted
mode, an empty strict MCP configuration unless an MCP server is explicitly
authorized, a bounded turn count, the narrowest built-in tool set, and only
exact pre-approved commands. Supply repository instructions in the assignment
because restricted mode does not auto-load project or user configuration.

Do not start a paid or capacity-consuming model request merely to test
authentication. If the host blocks an otherwise authorized network request,
use only its normal approval mechanism for the identical invocation. Never
solve connectivity by weakening Claude's permissions.

## 4. Inspect and independently verify

After Claude exits:

1. Inspect the process exit status, outer JSON subtype and errors, terminal
   reason, permission denials, session ID, structured output, and reported
   model usage.
2. Inspect `git status`, the complete diff, untracked files, and unexpected
   paths. Revert nothing automatically.
3. Review the implementation for scope, correctness, security, and repository
   conventions.
4. Run the most important authorized acceptance checks independently.
5. Classify the integrated outcome:
   - `complete`: the requested outcome is present and independently verified,
     with no material unfinished or unexpected work.
   - `partial`: useful in-scope progress is retained, but one or more material
     acceptance criteria remain unresolved.
   - `blocked`: no safe, integrable progress can be made because of authority,
     authentication, capacity, environment, or another stopping condition.

A missing or invalid structured report is an evidence defect, not automatically
a `partial` task outcome. Record it and classify the integrated work from all
available evidence. A cooldown or preflight stop is `blocked`, with the reason.

## 5. Correct once and report

When a narrow issue is correctable, resume the same session once. Restate the
complete original repository, ownership, prohibited actions, tool boundary,
and checks, then add only the remaining criterion. Repeat every relevant launch
flag. Stop if the installed CLI rejects a restriction on resume.

After any attempted delegation, capture post-task usage when available. Report
the requested model and effort separately from observed/effective values,
Claude's claims separately from Codex verification, all denials and unexpected
artifacts, unresolved work, capacity changes by named pool, and the final
classification.
