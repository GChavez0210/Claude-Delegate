# Claude Delegate

Claude Delegate is a Codex skill for assigning focused coding, investigation,
or review work to a locally installed Claude Code CLI. Codex defines the scope
and permissions, Claude performs the bounded assignment, and Codex reviews the
actual changes and independently verifies the result.

This repository is the development and distribution source. Installing it does
not modify an existing personal copy automatically.

## Prerequisites

- Codex with custom-skill support.
- Claude Code 2.1.259 or later available as `claude` on `PATH`.
- Your own authorized Claude subscription, Console/API account, or supported
  cloud-provider configuration.
- Git when repository status or worktrees are part of the task. Git for Windows
  is recommended for native Windows Claude Code use.
- A PTY-capable host only when automatic interactive `/usage` capture is used.

The skill runtime does not require Python. Repository maintainers running the
development validator need Python 3.10 or later; CI uses Python 3.12. Depending
on the platform, the launcher may be named `python`, `python3`, or `py -3`.

Claude Code installation and authentication are documented by Anthropic in
[Advanced setup](https://code.claude.com/docs/en/getting-started) and
[Authentication](https://code.claude.com/docs/en/authentication).

## Install

Clone or copy this repository to the `claude-delegate` folder under a Codex
skills directory. Common locations are:

```text
~/.codex/skills/claude-delegate
%USERPROFILE%\.codex\skills\claude-delegate
```

If `CODEX_HOME` is configured, use its `skills/claude-delegate` directory.
Restart or refresh Codex so it discovers the skill.

## Invoke

Ask Codex explicitly to use the skill and provide a bounded task:

```text
Use $claude-delegate to add regression tests for the parser bug. Claude may
edit only parser.test.ts and may run npm test -- parser.test.ts. Do not install
packages, commit, push, or access external systems.
```

```text
Use $claude-delegate for a read-only review of src/auth. Return findings only;
do not edit files or run write-capable commands.
```

Before an end-to-end run, Codex should make the proposed objective, owned paths,
authorized checks, model/effort, and expected usage concrete. A paid or
capacity-consuming request should not be launched merely to prove login.

To avoid duplicate context cost, Codex locates applicable instructions and
task-relevant documentation, then Claude reads only the files it needs. Codex
does not preload the same documents and reads one later only when authorization
or independent verification requires it. Claude returns a concise structured
report rather than a narrative recap.

## Permission and data boundary

The skill uses Claude Code restricted mode, explicit built-in tools,
deterministic denial for unattended prompts, and an empty strict MCP
configuration by default. Restricted mode is a boundary, not a blanket feature
ban: Codex includes task-required WebSearch, WebFetch, Chrome, or MCP tools and
pre-approves expected calls. It never authorizes permission bypass. Computer use
requires a supported interactive route; current Claude CLI computer use is
macOS-only and unavailable with non-interactive `-p`, while Windows support is
provided through Claude Desktop.

These controls reduce authority; they are not a full security sandbox. Claude
receives the assignment and relevant repository contents over the network. Run
only in a directory you trust and have placed in scope. A worktree separates
edits but does not isolate secrets or automatically include uncommitted work.
The owned-file list is enforced by instructions and post-run diff review, not a
per-file filesystem allowlist; use a minimized disposable checkout when other
repository files must be inaccessible.
Consumer and commercial data-handling terms differ; review Anthropic's
[data-usage documentation](https://code.claude.com/docs/en/data-usage).

Session persistence enables one bounded correction pass but stores local
session history. `--no-session-persistence` can be chosen when retention matters
more than resume; in that mode, correction-by-resume is unavailable.

## Authentication, billing, and usage

The portable skill supports explicitly authorized subscription, API, and
supported cloud-provider profiles. It stops when the active profile is
ambiguous. Personal rules—such as excluding a particular model—belong in the
installed local copy or repository instructions, not in the public default.

As of June 15, 2026, Anthropic states that `claude -p` and Agent SDK work on
subscription plans draws from a separate monthly Agent SDK credit. It must not
be inferred from ordinary interactive usage bars. Models, extended-context
variants, fast/extra-usage modes, and providers can have different availability
or billing behavior. The skill does not opt into separately billed behavior
without informed user authorization.

Claude's visible `/usage` pools and the host's Codex limits are captured by
default before and after delegation. Every visible pool is shown by name and
applicability, even when it cannot be confirmed as the print-mode pool. Reports
use an after-capacity ASCII bar plus exact before/after values, for example
`[##############------] 72% -> 70% remaining (-2 points)`. An already-configured
Remote Control connection does not by itself abort the isolated usage probe.
Missing telemetry is reported as unavailable rather than estimated.

## Known limitations

- Claude Code flags, aliases, effort support, auth fields, and usage UI are
  version-sensitive. The compact preflight reuses successful checks within a
  task and refreshes help only after a version change, uncertainty, or parser
  rejection.
- The documented launch boundary was statically checked on Windows with Claude
  Code 2.1.269. macOS/Linux shell quoting and the full restricted resume path
  have not yet been exercised end to end.
- An observed isolated run passed `--max-turns 10` but reported 12 outer
  turns. The skill therefore treats the flag as a proportional guardrail, not a
  verified strict ceiling.
- A prior disposable Windows capability probe produced three isolated files and
  passed 8 of 8 focused Node tests. That proves one bounded workflow, not broad
  runtime reliability or cross-platform compatibility.
- Structured output can fail even when useful work occurred. Codex therefore
  classifies the integrated result from the diff, checks, process result, and
  report instead of trusting any single signal.
- There is no custom runner, MCP server, daemon, or persistent job manager.
  Repeated cross-shell quoting or normalization failures would be evidence for
  a future helper; none is currently justified.

## Development validation

Run the dependency-free core checks and the no-model local CLI probe with:

```text
python scripts/validate_skill.py --check-cli
```

Replace `python` with `python3` or `py -3` when that is the available launcher.

For full YAML, draft-7 metaschema, and positive/negative report-fixture
validation, install the development-only requirements in an isolated
environment and run:

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py --require-deps --check-cli
```

The included GitHub Actions workflow is configured to run the full package
validation on Windows, macOS, and Linux. It does not install Claude Code or send
a model request. Its first hosted run remains pending until these changes are
pushed. Any end-to-end Claude test should use a disposable data-free workspace
and an explicitly authorized, concrete task.

## License and trademarks

Released under the [MIT License](LICENSE).

This project is unofficial and is not affiliated with or endorsed by Anthropic
or OpenAI. Claude and Claude Code are marks of Anthropic; Codex and OpenAI are
marks of OpenAI.
