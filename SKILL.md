---
name: claude-delegate
description: Delegate a bounded coding, investigation, or review task to a local Claude Code CLI when the user requests Claude Code delegation. Codex scopes the work, grants only the needed permissions, and independently verifies the result.
---

# Delegate to Claude Code

Use Claude to offload bounded work and conserve Codex context. Keep setup short;
Codex remains responsible for authorization, integration, and verification.

## Fast path

1. **Scope.** Locate applicable `AGENTS.md`, `CLAUDE.md`, and relevant docs
   without reading them. Give Claude their paths; it reads only what it needs.
   Codex reads one only for authorization or disputed verification—never by
   default in both agents. Define the objective, owned paths, prohibitions,
   acceptance criteria, and exact checks.
2. **Pre-authorize.** Predict every needed tool and command. Obtain missing user
   authority once, set availability with `--tools`, and pre-approve expected
   calls with `--allowedTools`. Implementation commonly needs `Read`, `Glob`,
   `Grep`, `Write`, and `Edit`; include `Bash` only with exact authorized rules.
   Use `acceptEdits` for implementation and `dontAsk` for read-only work.
3. **Preflight once.** Check version, status/instruction paths, and filtered auth
   JSON containing only login state, method, provider, and subscription. Check
   provider environment presence only if ambiguous, help only after version or
   flag uncertainty, and usage only when requested or material. Reuse the result
   unless the workspace, CLI, profile, or boundary changes.
4. **Launch.** Pass the user request, boundaries, and documentation paths because
   Claude does not inherit the Codex conversation. Tell Claude to return only
   the structured report, with a one-sentence summary and one-line check
   outcomes. Load [references/report-schema.json](references/report-schema.json)
   as launch data, not documentation. Use this boundary:

   ```text
   claude -p --output-format json --json-schema <schema> --model <model>
     --permission-mode <acceptEdits|dontAsk> --permission-prompts none
     --restricted --mcp-config {"mcpServers":{}} --strict-mcp-config
     --no-chrome --max-turns <N> --tools <needed-tools>
     --allowedTools <each expected tool or exact command rule>
   ```

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
