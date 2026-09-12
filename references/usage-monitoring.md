# Usage and billing monitoring

Capture Claude execution capacity and Codex orchestration capacity separately.
Telemetry is best-effort unless the user explicitly requires a strict capacity
gate. Missing data means unavailable, not zero usage.

On the default fast path, capture the host's read-only Codex limits and Claude's
visible `/usage` pools before and after delegation. Display every visible pool;
label its applicability instead of hiding interactive or uncertain pools merely
because the print-mode pool is unavailable.

## Identify the relevant Claude pool

First identify the authorized authentication profile and active provider.
Subscription, API, Bedrock, Vertex, Foundry, and gateway usage have different
limits and billing sources.

As of June 15, 2026, Anthropic documents `claude -p` and Agent SDK work on
subscription plans as drawing from a separate monthly Agent SDK credit rather
than ordinary interactive limits. Therefore:

- record every visible pool by its displayed name;
- prefer the Agent SDK/monthly pool when it is shown for a print-mode launch;
- never infer print capacity from an unrelated five-hour, weekly, token, cost,
  or interactive-usage value;
- do not call a run "included" or "free" merely because authentication uses a
  subscription.

## Claude snapshot

By default, when interactive capture is available:

1. Start a bounded temporary interactive Claude session with no task prompt,
   restricted tools, empty strict MCP configuration, and guaranteed cleanup.
2. Send `/usage`, wait for the view, and record only visibly returned fields.
3. Dismiss the view and exit without submitting a work prompt.

Some CLI builds may still show a workspace-trust prompt in restricted
interactive mode or display an unsolicited Remote Control connection attempt.
Confirm trust only after independently verifying that the disposable workspace
is the exact user-authorized directory. Remote Control is legitimate and its
presence alone is not a capture failure. If already configured, continue the
isolated probe unless unexpected remote input or permission changes appear;
then exit only the probe. Do not actively enable Remote Control merely for
telemetry. This does not restrict the assignment's authorized capabilities.

Observed on Windows with Claude Code 2.1.269: a sandboxed `/usage` load failed,
while the identical restricted probe with Claude-service network access
succeeded with `/rc active` and displayed current-session, current-week, and
usage-credit pools. Diagnose the usage request's network access separately from
Remote Control status.

`/usage` and other background commands can themselves cause small token usage.
Do not describe this check as cost-free. Its terminal layout is version- and
plan-dependent; if capture or parsing is unreliable, report it as unavailable
and tell the user how to inspect `/usage` manually.

Normalize when possible:

```text
captured_at: timestamp with timezone
capture_status: available | unavailable | timed_out
authentication_profile: subscription | api | bedrock | vertex | foundry | other
pools:
  - name
    applicability: print | interactive | api | unknown
    used_percent
    remaining_percent
    resets_at
warnings: visible messages only
```

Claude status-line `rate_limits` fields can expose five-hour and seven-day usage
for some subscribers, but only after an API response. They are not a no-cost
source for a pre-launch snapshot and may not represent the monthly Agent SDK
pool.

## Codex snapshot

Use the host's read-only Codex usage-limit capability when available. Never
consume a reset credit merely to inspect capacity. Record the plan, each named
window or limit ID, used and remaining percentages, reset times, and whether a
reset credit exists.

## Gate and compare

- If an observed applicable Claude limit is reached, do not launch. Classify
  the attempt as `blocked` and report the reset time.
- If the relevant pool is unavailable, proceed only when the task's size,
  billing profile, and user authorization make that uncertainty acceptable.
- If Codex capacity is too low for independent review, reduce scope or wait.
- Do not invent universal low-capacity thresholds.
- Compare matching named pools and windows only.
- Report every visible Claude pool by name and applicability even when no pool
  can be confirmed as the one used by print mode.
- Present remaining capacity on a 100-to-0 scale. When only used percentage is
  returned, calculate `remaining = 100 - used`.
- Display every available remaining percentage as a fixed-width, ASCII-only
  depletion bar followed by the numeric value. Use 20 cells, `#` for remaining
  capacity, and `-` for depleted capacity; round the bar to the nearest cell
  while preserving the observed percentage in the label. For example:

  ```text
  Agent SDK [##############------] 72% -> 70% remaining (-2 points)
  Five-hour [#####---------------] 23% -> 23% remaining (no visible change)
  ```

  Clamp calculated values to 0-100. If a percentage is unavailable, do not
  estimate a bar; report `<pool> [????????????????????] unavailable`.
- Calculate `change = after remaining - before remaining`; consumption is
  negative and a reset is positive. Report percentage-point changes.
- An unchanged rounded value means no visible change, not zero consumption.

Keep token counts, turn counts, locally estimated cost, subscription limits,
and actual billing as separate facts. Never describe `total_cost_usd` as an
incremental confirmed charge for a subscription-backed run.
