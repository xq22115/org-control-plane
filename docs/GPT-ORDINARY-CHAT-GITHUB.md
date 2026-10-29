# GPT ordinary-chat × GitHub plugin strength

Version: `2026-10-29.4`
Owner contracts live in `xq22115/braintrust` `.chatgpt/`.

## Root cause (why answers stayed shallow)

1. **Depth was keyword-gated** — ultra/strict overlays waited for `深度思考更久` / `think longer`.
2. **Five-angle goal compile was buried** inside a long core file and often never demand-loaded after preflight.
3. **GitHub plugin was treated as storage/CI**, not as the ordinary-chat **thinking substrate**.
4. **Wall-clock theater ≠ depth** — fixed waiting does not deepen reasoning; useful search, falsification, and plugin read-back do.

## Architecture fix (thinking link)

For every **substantive** ordinary-chat turn when the GitHub app/plugin is connected and callable:

1. Bounded preflight: `.chatgpt/github-preflight.json`
2. Load thinking link: `.chatgpt/ordinary-chat-plugin-thinking-link.md` + `.json`
3. Compile goal through **five angles**: `.chatgpt/ordinary-chat-five-angle-goal.json`
4. Deepen with plugin calls (`get_me` / `list_*` / `search_*` / exact reads) via `.chatgpt/ordinary-chat-github-loop.md`
5. `CONSTRUCT → FALSIFY → SYNTHESIZE` until no material delta; sleep/queue = zero depth credit

Wired from: bootstrap, profile, capabilities (`plugin_thinking_link` in `default_always_on`), core, preflight, **context-policy module**, global acceptance D7.
`.agents/skills/ordinary-chat-ultra-deliberation/SKILL.md` is an **intensifier**, not the only depth switch.

Landed: `xq22115/braintrust` PR #925 merged to `main` as `9101f6a1225b4a355fd04ea626b8043214ee00ca` (2026-10-29).


## Deepen (2026-10-29.4) — machine router + acceptance

After #925, prose/bootstrap already named the thinking link, but the **machine router** still lagged:

1. `.chatgpt/ordinary-chat-context-policy.json` now registers `modules.plugin_thinking_link` as scoped `default=true` (substantive turns when GitHub callable; **not** byte `default_preload`).
2. `ultra_deliberation` role = `intensifier_after_plugin_thinking_link`.
3. Capability registry test + new contract test lock `default_always_on = [github_connector, plugin_thinking_link]`.
4. Global acceptance adds **D7** `plugin_thinking_link_five_angle_default_on` with truth_rules forbidding keyword-gated depth.

Landed track: braintrust PR #926 (open/merging). EFFECT_VERIFIED on ChatGPT ordinary-chat product remains **NOT RUN**.

## Product honesty

`CONFIGURED ≠ CONNECTED ≠ CALLABLE ≠ EFFECT_VERIFIED`
Repository text cannot change OpenAI server-side reasoning budgets or hard safety. Soft over-refusal may retry ≤2 alternate GitHub/search routes; never claim provider hard unlock.

## Five angles (SSOT)

| ID | Lens |
|---|---|
| A1 | literal_request |
| A2 | desired_end_state |
| A3 | constraints_and_non_goals |
| A4 | causal_owner_and_runtime |
| A5 | github_and_evidence_identity |

Compile fields: `PRIMARY_TASK`, `DESIRED_END_STATE`, `NEGATIONS`, `HARD_CONSTRAINTS`, `ACCEPTANCE_TESTS`. One load-bearing dissent blocks irreversible action; majority vote ≠ truth.

## Must-keep open work (post 5-agent debate 2026-10-29)

| PR | Why keep |
|---|---|
| #837 | Ordinary-chat connected-app + GitHub connector action-contract (rebase onto main) |
| #920 | Cross-AI Actions demand-load discovery bridge |
| #916 | Dependabot group — KEEP draft; do not blind-merge SHA mega-pin |

Merged: #918 (truth-guard), #919 (SHA pagination), #925 (plugin thinking-link + five-angle). Closed: #903, #922.

## Canary before claiming boost

1. `get_me` succeeds on the live GitHub connector
2. One `list_*` or `search_*` returns repo-scoped data
3. Thinking-link + five-angle contracts are retrievable from `braintrust@main`
4. Receipt marks `actions_capability_preserved=true` and `five_angle_compiled=true` when substantive

## Output quality

Lead with effect + evidence URL/SHA. Separate soft-pass continues from provider hard limits in every user-facing claim.
