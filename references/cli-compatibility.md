# Claude Code CLI compatibility

This skill targets Claude Code 2.1.259 or later. Feature-detect every
security-relevant flag because Claude Code changes frequently.

## Verified snapshot

Locally inspected on 2026-09-11 with Claude Code 2.1.268 on Windows:

- `-p` / `--print` and JSON output;
- `--json-schema` structured output;
- `--model` and `--effort`;
- `acceptEdits` and `dontAsk` permission modes;
- `--permission-prompts none`;
- `--restricted`;
- `--tools`, `--allowedTools`, and `--disallowedTools`;
- `--mcp-config` and `--strict-mcp-config`;
- `--resume` and `--fork-session`;
- `claude auth status` JSON output.

`--max-turns` was accepted by the local parser and is documented in the current
official CLI reference, but was not displayed in that build's `--help`. Check it
without a model request using `claude --max-turns 1 --help`, then still treat
runtime enforcement as unverified until observed in a real authorized run.

The local authentication JSON contained `loggedIn`, `authMethod`,
`apiProvider`, and `subscriptionType`. These field names are observed behavior,
not a stable public contract. Parse auth output locally and emit only those
allowlisted fields. Never log raw output, identity fields, organization IDs,
paths, or credentials. If the host cannot safely filter the result, treat the
profile as unverified instead of exposing it.

Do not run `claude auth status` as a standalone captured command. Parse and
project the allowlisted keys within the same host invocation. For example, in
PowerShell:

```powershell
claude auth status --json |
  ConvertFrom-Json |
  Select-Object loggedIn, authMethod, apiProvider, subscriptionType |
  ConvertTo-Json -Compress
```

In Bash, use an already-installed trusted JSON parser such as `jq` to select the
same four keys. Do not install a parser merely for preflight.

## Version-sensitive behavior

- `--restricted` requires Claude Code 2.1.248 or later.
- `--permission-prompts none` requires 2.1.259 or later.
- Invalid structured-output schemas fail at startup in 2.1.205 or later; older
  versions could silently ignore them.
- `--json-schema` uses JSON Schema draft 7.
- `--tools` restricts built-in tools; it does not restrict MCP tools.
- `--allowedTools` pre-approves matching calls; it does not limit availability.
- Print mode skips the workspace trust dialog. Run it only in a directory the
  user placed in scope.
- Restricted mode ignores user, project, and local settings, but managed
  settings and explicit `--settings` still apply.
- Resume restores conversation state. Repeat the complete permission and scope
  boundary on the command line and in the correction prompt.

If any required behavior is absent or ambiguous, upgrade or stop. Do not weaken
the boundary to preserve compatibility.

## Official references

- [CLI reference](https://code.claude.com/docs/en/cli-usage)
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
- [Permissions](https://code.claude.com/docs/en/permissions)
- [Authentication](https://code.claude.com/docs/en/authentication)
- [Model configuration](https://code.claude.com/docs/en/model-config)
- [Structured outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)
- [Usage and costs](https://code.claude.com/docs/en/costs)
- [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
