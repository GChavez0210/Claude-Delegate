---
name: claude-delegate
description: Delegate a bounded coding, investigation, or review task to a local Claude Code CLI when the user requests Claude Code delegation. Codex scopes the work, grants only the needed permissions, and independently verifies the result.
---

# Delegate to Claude Code

Offload bounded work to Claude with minimal Codex context. Codex remains
responsible for authorization, integration, and verification.

## Fast path

1. **Scope.** Locate applicable `AGENTS.md`, `CLAUDE.md`, and relevant docs
   without reading them. Give Claude their paths; it reads only what it needs.
   Codex reads one only for authorization or disputed verification—never by
   default in both agents. Define the objective, owned paths, prohibitions,
   acceptance criteria, and exact checks. Preserve existing work; do not edit
   Claude's checkout while it runs. Use a worktree for concurrent or dirty work
   and account for uncommitted changes.
2. **Pre-authorize.** Predict every needed tool and command. Obtain missing user
   authority once, set availability with `--tools`, and pre-approve expected
   calls with `--allowedTools`. Implementation commonly needs `Read`, `Glob`,
   `Grep`, `Write`, and `Edit`; include `Bash` only with exact authorized rules.
   Use `acceptEdits` for implementation and `dontAsk` for read-only work.
3. **Preflight once.** Check version, status/instruction paths, and auth JSON
   limited to login state, method, provider, and subscription. Check provider
   variables only for ambiguous auth and help only on version/flag uncertainty.
   Stop on profile or billing ambiguity. Show available
   host/Codex limits before and after delegation
   as `Name [################----] 80% remaining`: 20 cells, `#` remaining, `-`
   depleted, and negative percentage-point consumption. Show unknown values as
   `[????????????????????] unavailable`. Probe Claude `/usage` only when requested
   or material. Keep routine preflight silent except for blockers and capacity
   bars. Reuse other results unless the workspace, CLI, profile, or boundary
   changes.
4. **Launch.** Pass the request, boundaries, and documentation paths. Require
   only the structured report, with a one-sentence summary and one-line check
   outcomes. Load [references/report-schema.json](references/report-schema.json)
   as launch data, not documentation. Use this boundary:

   ```text
   claude -p --output-format json --json-schema <schema> --model <model>
     --permission-mode <acceptEdits|dontAsk> --permission-prompts none
     --restricted --mcp-config {"mcpServers":{}} --strict-mcp-config
     --no-chrome --max-turns <N> --tools <needed-tools>
     --allowedTools <each expected tool or exact command rule>
   ```

   Choose `<N>` proportionally—there is no universal 8-turn cap—and leave one
   turn for the structured report.

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

Report `complete`, `partial`, or `blocked`, separating Claude's claims from
Codex verification. Do not commit, push, publish, deploy, install dependencies,
access unrelated systems, or remove user work without explicit authorization.

## Read details only when needed

- [Assignment and permissions](references/assignment-and-permissions.md): shell
  quoting, complex tool rules, permission troubleshooting, or resume failures.
- [CLI compatibility](references/cli-compatibility.md): version/flag mismatch.
- [Model routing](references/model-routing.md): non-obvious model or effort
  choice.
- [Usage monitoring](references/usage-monitoring.md): requested usage, billing,
  or capacity reporting.
