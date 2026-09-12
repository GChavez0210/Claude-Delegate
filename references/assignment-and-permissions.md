# Assignment, permissions, launch, and correction

## Assignment contract

Claude does not inherit the Codex conversation. Include all material context:

```text
Repository or workspace:
<absolute path and starting Git state>

Repository instructions and relevant documentation for Claude to read:
<paths located by Codex; Claude reads only what the task requires>

Objective:
<one concrete outcome>

Owned files or modules:
<exact scope>

Constraints and prohibited actions:
<repository, database, network, commit, push, deployment, dependency, and
side-effect limits>

Acceptance criteria and authorized checks:
<observable behavior plus exact focused test, lint, type, and format commands>

You share this project with other contributors. Preserve unrelated work. Do not
change files outside the owned scope. Report instruction files found, changed
files, every check with its actual exit status, permission denials, unexpected
changes, and unfinished work. Do not claim a check passed unless you ran it and
observed the result. Return only the structured report. Keep the summary to one
sentence and every check outcome to one line.
```

Name exact checks instead of asking for "production quality." Start focused and
broaden only when failures, shared behavior, or material risk justify it. Codex
should locate relevant documentation without preloading it; avoid making both
agents ingest the same material. Codex may read a specific document when needed
to establish authority or independently resolve a disputed verification fact.

## Complete the tool budget before launch

Avoid preventable permission failures by deriving the tool budget from the
objective and every acceptance check before starting Claude:

1. List the built-in tools the work genuinely needs. Ordinary implementation
   commonly needs `Read`, `Glob`, `Grep`, `Write`, and `Edit`; add `Bash` only
   when an authorized check or operation requires it.
2. Put the complete availability boundary in `--tools`.
3. Put each expected built-in call and each exact authorized shell matcher in
   `--allowedTools` as a distinct argument. Availability alone does not
   pre-approve a call.
4. If the task predictably needs installation, network, Git mutation, or another
   separately consequential action, obtain that authority once before launch.

Do not deliberately under-authorize a known requirement and wait for Claude to
discover it. Conversely, do not add speculative tools or broad command
wildcards merely to avoid prompts. If an already user-authorized action was
accidentally omitted, correct only the missing rule and resume once. A denial
caused by missing user authority still requires the user; permission bypass is
never a recovery mechanism.

## Permission boundary

For the documented baseline (Claude Code 2.1.259 or later):

- Use `--restricted` to ignore user/project/local settings, confine file tools
  to working directories, refuse bypass mode, and remove command/code execution
  and WebFetch unless `--tools` explicitly names them.
- Use `--permission-prompts none` so unattended actions that would prompt are
  denied instead of waiting or consulting an unspecified host.
- Use `acceptEdits` only for authorized implementation. Use `dontAsk` for
  read-only investigation and review.
- Restrict built-in availability with `--tools`. `--allowedTools` only
  pre-approves matching calls; it is not an availability boundary.
- Pre-approve only exact authorized commands. Quote each rule as one shell
  argument and verify matcher syntax against current help/documentation.
- Pass `--mcp-config '{"mcpServers":{}}' --strict-mcp-config` unless an
  explicitly authorized MCP server is required.
- Add `--no-chrome` unless browser integration is in scope.
- Never pass either dangerous permission-bypass flag.

Restricted mode does not auto-load repository `CLAUDE.md` or ordinary settings.
Name applicable instruction and documentation paths in the assignment and give
Claude `Read` access so it can load only what it needs. If `Read` is unavailable,
pass required contents once rather than having both agents load them. Managed
settings still apply. Do not add a temporary settings file unless a concrete
required setting has been inspected and validated.

If the installed CLI lacks a required boundary flag, upgrade it or stop for
sensitive/unattended work. Do not improvise an undocumented `--setting-sources`
value or silently fall back to a weaker boundary.

## Launch contract

Confirm flags from current help when the CLI version changed, a flag is
uncertain, or the parser rejected it; do not repeat an unchanged successful
check before every launch. The effective argument list must include:

```text
-p
--output-format json
--json-schema <compact schema JSON>
--model <authorized model>
[--effort <verified supported effort>]
--permission-mode <acceptEdits|dontAsk>
--permission-prompts none
--restricted
--mcp-config {"mcpServers":{}}
--strict-mcp-config
--no-chrome
--max-turns <bounded positive integer>
--tools <comma-separated built-in tools>
[--allowedTools <one or more exact approved rules>]
```

Pass the assignment on standard input or as the final prompt argument. Preserve
each variadic tool rule as a distinct argument; shell quoting differs between
PowerShell and POSIX shells.

PowerShell shape:

```powershell
$schema = (Get-Content -Raw '<skill>\references\report-schema.json' |
  ConvertFrom-Json | ConvertTo-Json -Depth 20 -Compress)
$claudeArgs = @('-p', '--output-format', 'json', '--json-schema', $schema,
  '--model', $model, '--permission-mode', $permissionMode,
  '--permission-prompts', 'none', '--restricted', '--mcp-config',
  '{"mcpServers":{}}', '--strict-mcp-config', '--no-chrome',
  '--max-turns', "$maxTurns", '--tools', $tools)
if ($effort) { $claudeArgs += @('--effort', $effort) }
if ($allowedToolRules.Count -gt 0) {
  $claudeArgs += @('--allowedTools') + $allowedToolRules
}
$assignment | & claude @claudeArgs
```

Bash shape:

```bash
schema=$(cat "$skill/references/report-schema.json")
claude_args=(-p --output-format json --json-schema "$schema"
  --model "$model" --permission-mode "$permission_mode"
  --permission-prompts none --restricted
  --mcp-config '{"mcpServers":{}}' --strict-mcp-config --no-chrome
  --max-turns "$max_turns" --tools "$tools")
if [[ -n ${effort:-} ]]; then claude_args+=(--effort "$effort"); fi
if ((${#allowed_tool_rules[@]})); then
  claude_args+=(--allowedTools "${allowed_tool_rules[@]}")
fi
printf '%s' "$assignment" | claude "${claude_args[@]}"
```

Omit `--allowedTools` when there are no rules. Do not add `--max-budget-usd` to
a subscription profile; API spending controls belong only to an explicitly
authorized API profile. Leave at least one turn of headroom for structured
output.

Treat the process exit status, outer JSON subtype/errors, presence of
`structured_output`, Claude's task status, reported checks, filesystem changes,
and Codex verification as separate evidence. A successful outer result without
structured output is a report failure.

## One safe correction pass

Resume only for a narrow issue. The correction prompt must repeat the full
original repository, instruction, ownership, prohibited-action, tool, and check
boundaries before naming the remaining criterion. Repeat every relevant flag,
including `--restricted`, `--permission-prompts none`, MCP restrictions, model,
effort, tools, exact command rules, and turn cap.

If resume rejects a restriction, stop. Do not retry with a weaker boundary.
Codex may make an independently authorized narrow correction or ask the user.
Inspect the new diff and rerun relevant checks after the single correction pass.
