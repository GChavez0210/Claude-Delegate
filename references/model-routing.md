# Working mode and model routing

## Working mode

- **Sequential implementation:** use the current checkout and do not edit it
  while Claude runs.
- **Concurrent or dirty-checkout implementation:** prefer a separate Git
  worktree. Confirm its starting commit and explicitly account for uncommitted
  changes, which are not copied automatically.
- **Investigation or review:** prohibit edits, use `dontAsk`, and expose only
  required read tools. Do not use plan mode merely for read-only work.
- **Disposable evaluation:** use a fresh data-free workspace or worktree and
  state whether its artifacts will be retained.

A worktree separates edits; it is not a security sandbox.

## Choose capability before aliases

Use these as defaults, then verify what the installed CLI, provider, plan, and
organization actually make available:

- **Haiku:** repository discovery, concise summaries, formatting, and simple
  read-only or mechanical work with strong acceptance criteria.
- **Sonnet:** ordinary implementation, debugging, focused tests, and bounded
  multi-file refactors.
- **Opus:** difficult architecture, concurrency, security, ambiguous
  multi-module behavior, or root-cause analysis where deeper reasoning is
  likely to change the result.

Aliases resolve differently across providers and can change over time. Use an
alias when tracking the provider's current recommendation is desirable; use a
full model name when reproducibility matters. Do not configure an automatic
fallback when the user selected a model explicitly.

## Effort

Effort support depends on the resolved model, not just the family alias.
Current Anthropic documentation lists:

- Fable 5/5.1, Opus 5/4.8/4.7, and Sonnet 5: `low`, `medium`, `high`, `xhigh`,
  and `max`.
- Opus 4.6 and Sonnet 4.6: `low`, `medium`, `high`, and `max`; `xhigh` is
  silently clamped to `high`.
- Models not listed, including the current Haiku entry, do not have documented
  effort support.

Omit `--effort` when support is not verified. If the user requires an exact
effort that the resolved model may clamp or reject, stop and explain the
uncertainty rather than claiming it was applied.

Lower effort favors latency and capacity; higher effort favors deeper
reasoning. Do not escalate because a command was denied, authentication failed,
a dependency is absent, or a test exposed an ordinary bug.

Record separately:

- `requested_model`: the `--model` value;
- `requested_effort`: the `--effort` value, or omitted;
- `models_observed`: every model in outer JSON model-usage metadata;
- `effective_effort`: only when directly observed.

Observed helper, routing, or fallback models do not retroactively change what
was requested.
