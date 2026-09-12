---
name: claude-delegate
description: Delegate a bounded coding, investigation, or review task to a local Claude Code CLI when the user requests Claude Code delegation. Codex scopes the work, grants only the needed permissions, and independently verifies the result.
---

# Delegate to Claude Code

Delegate bounded work with minimal Codex context; Codex retains authorization,
integration, and verification.

## Fast path

1. **Scope.** Locate applicable `AGENTS.md`, `CLAUDE.md`, and relevant docs
   without reading; Claude reads only what it needs. Codex reads a file only
   for authorization or disputed verification. Define objective, owned paths,
   prohibitions, acceptance criteria, and exact checks. Preserve existing work;
   do not edit Claude's checkout while it runs. Use a worktree for concurrent or
   dirty work and account for uncommitted changes.
2. **Pre-authorize.** Budget every task-required command and capability,
   including web, browser, or MCP access. Obtain missing authority once; expose
   built-ins with `--tools` and pre-approve calls with `--allowedTools`.
   Implementation commonly needs `Read`, `Glob`, `Grep`, `Write`, and `Edit`;
   add `Bash` only with exact rules. Use `acceptEdits` for implementation and
   `dontAsk` for read-only work.
3. **Preflight once.** Check version, status/instruction paths, and auth JSON
   limited to login state, method, provider, and subscription. Inspect provider
   variables only for ambiguous auth and help only on version/flag uncertainty;
   stop on profile or billing ambiguity. Capture Claude `/usage` and host/Codex
   limits before and after delegation. Report every visible pool as
   `Name [################----] 80% -> 78% remaining (-2 points)`: 20 cells,
   `#` remaining and `-` depleted; use `[????????????????????] unavailable` only
   when no percentage is visible. Keep preflight silent except blockers and
   capacity bars; reuse results unless workspace, CLI, profile, or boundary
   changes.
4. **Launch.** Pass the request, boundaries, and documentation paths. Require
   only the structured report, with a one-sentence summary and one-line check
   outcomes. Load [references/report-schema.json](references/report-schema.json)
   as launch data, not documentation. Use this boundary:

   ```text
   claude -p --output-format json --json-schema <schema> --model <model>
     --permission-mode <acceptEdits|dontAsk> --permission-prompts none
     --restricted --mcp-config <authorized-or-empty> --strict-mcp-config
     [--chrome|--no-chrome] --max-turns <N> --tools <task-tools>
     --allowedTools <each expected tool or exact command rule>
   ```

   Default `<N>` to 20; raise it before longer tasks. It is a proportional
   guardrail, not a guaranteed ceiling; leave report headroom.

   Prefer Haiku for simple mechanical work, Sonnet for ordinary implementation,
   and Opus only when difficult reasoning warrants it. Honor the user's model;
   omit effort unless supported. Never use bypass permissions or opt into
   separately billed behavior without informed authorization.
5. **Verify.** Inspect exit status, errors, session ID, structured output,
   denials, model usage, complete diff/status, and unexpected paths. Review the
   actual work and independently run the most important authorized check; do
   not reread whole documentation sets. Claude's report is evidence, not proof.

If an action already authorized by the user was denied because the tool budget
was incomplete, correct only that rule and resume once with the full boundary.
If authority itself is missing, ask the user. Never weaken restricted mode.

Report status first and briefly. Omit routine setup; include material changes,
verification, failures/denials, unfinished work, and capacity bars. Do
not commit, push, publish, deploy, install dependencies, access unrelated
systems, or remove user work without explicit authorization.

## Read details only when needed

- [Assignment and permissions](references/assignment-and-permissions.md): shell
  quoting, external capabilities, permissions, or resume failures.
- [CLI compatibility](references/cli-compatibility.md): version/flag mismatch.
- [Model routing](references/model-routing.md): non-obvious model or effort
  choice.
- [Usage monitoring](references/usage-monitoring.md): capture trouble, billing,
  pool applicability, or capacity gates.
