# Usage and billing monitoring

Capture Claude execution capacity and Codex orchestration capacity separately.
Telemetry is best-effort unless the user explicitly requires a strict capacity
gate. Missing data means unavailable, not zero usage.

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

When automatic capture is available and proportionate:

1. Start a bounded temporary interactive Claude session with no task prompt,
   restricted tools, empty strict MCP configuration, and guaranteed cleanup.
2. Send `/usage`, wait for the view, and record only visibly returned fields.
3. Dismiss the view and exit without submitting a work prompt.

Some CLI builds may still show a workspace-trust prompt in restricted
interactive mode or display an unsolicited Remote Control connection attempt.
Confirm trust only after independently verifying that the disposable workspace
is the exact user-authorized directory. Do not enable or retry Remote Control or
another unexpected integration merely to obtain telemetry; if it does not fail
closed, exit and report usage as unavailable.

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
- Present remaining capacity on a 100-to-0 scale. When only used percentage is
  returned, calculate `remaining = 100 - used`.
- Display every available remaining percentage as a fixed-width, ASCII-only
  depletion bar followed by the numeric value. Use 20 cells, `#` for remaining
  capacity, and `-` for depleted capacity; round the bar to the nearest cell
  while preserving the observed percentage in the label. For example:

  ```text
  Agent SDK [##############------] 70% remaining
  Five-hour [#####---------------] 23% remaining
  ```

  Clamp calculated values to 0-100. If a percentage is unavailable, do not
  estimate a bar; report `<pool> [????????????????????] unavailable`.
- Calculate `change = after remaining - before remaining`; consumption is
  negative and a reset is positive. Report percentage-point changes.
- An unchanged rounded value means no visible change, not zero consumption.

Keep token counts, turn counts, locally estimated cost, subscription limits,
and actual billing as separate facts. Never describe `total_cost_usd` as an
incremental confirmed charge for a subscription-backed run.
