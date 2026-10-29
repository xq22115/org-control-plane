# RE-AUDIT 3× AFTER — xq22115 (as_of 2026-10-29)

Status: **PARTIAL→materially VERIFIED on noise/closeout gates**; plan-locked items remain BLOCKED (Free org rulesets / private auto-merge).

## Goal lock

- Primary: reverse-engineer org debt; ≥3× improvement without capability downgrade.
- Hard constraints: Actions=all, no SHA pin mandate, GPT plugin/App automation intact, 0 required reviews preserved.

## Multipliers (live)

| Metric | Before | After | Factor |
|---|---:|---:|---:|
| braintrust branches (full ref count) | 527 | 24 | **21.96×** |
| braintrust open PRs (mostly stale drafts) | ~203 | 19 | **10.68×** |
| demo-repository branches | 71→94 page noise | 14 | **≥5×** |
| ai-thinking-debate-skills-lab branches | ~94–100 | 21 | **~4.5×** |
| cursor branches | 17+ | 7 | **≥2×** (prior pass already cleaned) |
| Post-Merge closeout | SyntaxError + unbounded stale BLOCKED redispatches | success; `reconcile_candidates: []` | **noise floor cleared** |

Evidence JSON: `evidence/after_3x_metrics.json` (this repo).

## What changed (preserve-and-improve)

1. **Hotfix** `verify_delivery_closure.py` syntax seam corruption → [PR #924](https://github.com/xq22115/braintrust/pull/924) squash-merged; `compile()` OK on main.
2. **Closeout bounds** kept: `reconcile_max_age_days=14`, `reconcile_incomplete_limit=2`, terminal classifications skip; audit run [40856320864](https://github.com/xq22115/braintrust/actions/runs/40856320864) success with empty reconcile queue.
3. **Stale draft hygiene**: closed **131** drafts (`updated ≤2026-10-15`); recent/active drafts untouched.
4. **Branch purge** (merged + >14d stale, never open-PR/protected): braintrust 239 + prior wave; demo 57; ai-lab 73; cursor 10; rescue 6.
5. **Auto-merge** enabled where plan allows; private Free-org canary remains API-false (GitHub plan lock).
6. **Required-checks P1** revalidated: 0 name mismatches vs 223 active workflows (prior finding = pagination false positive).

## Capability read-back (must stay)

- Org Actions: `enabled_repositories=all`, `allowed_actions=all`
- No new required reviews / SHA pin / Actions restriction introduced
- 11 GitHub Apps unchanged; GPT connector path preserved

## Remaining (explicit, not silent)

| Item | State | Why |
|---|---|---|
| Org private rulesets / BP enforce | BLOCKED | Free org plan |
| Private `allow_auto_merge` on canary | BLOCKED | Free org + private repo |
| `permissions: write-all` on 6 audit workflows | PARTIAL | Narrowing is next; not cut this pass to avoid GPT/admin false fails |
| Dual vercel canary (org + pixel) | PARTIAL | Keep org canary as control-plane witness; pixel as Pro runner |
| `pull_request_target` trio | PARTIAL | Needs checkout-trust audit; no blind delete |

## Acceptance

- [x] ≥3× branch **or** open-PR noise (both exceeded)
- [x] Closeout green + script compiles
- [x] No Actions capability downgrade
- [ ] Plan-locked rulesets (external)
- [ ] write-all narrowing (queued, reversible)
