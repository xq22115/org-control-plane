# xq22115 org-control-plane

Organization control plane after Enterprise/Team → **Free org** + personal **Pro (`xq22115-pixel`)**.

**as_of:** 2026-10-29  
**Principle:** do not blind-copy Enterprise locks; place each control where the current plan can enforce it.

## Architecture (solo world-class)

| Tier | Where | What lives here |
|---|---|---|
| A. Brand / namespace | Org `xq22115` (Free) | Public OSS, soft integrity rulesets, Actions allow-all for GPT/agent automation, org Apps |
| B. Private product + enforceable gates | User `xq22115-pixel` (Pro) | Private repos that need Rulesets / Environments / CODEOWNERS enforcement |
| C. Policy-as-code | Repo `.github/` (esp. `xq22115/braintrust`) | Workflows, `required-checks.yml`, `agent-core-policy.yml` — still run on Free; **cannot** server-enforce private branch locks on Free org |
| D. Shared templates | This repo + `workflow-templates/` | Thin reusable starters — not a clone of 200+ braintrust workflows |

## Patterns used (adapted)

1. GitHub Docs — reusable workflows + org `.github` templates; Free org private repos lose branch protection.
2. Solo Pro placement — private governed work under Personal Pro when org is Free.
3. Soft integrity rulesets on **public** repos only (block force-push/delete; **0** required reviews) so GPT/agent automation stays unblocked.

## Do not copy from Enterprise

- Org-wide rulesets (needs Team+)
- Private-repo rulesets / classic branch protection on Free org
- Private environment wait timers / required reviewers (Enterprise)
- Blind required-status walls that freeze agent push without a green aggregate job

## Latest strengthen pass

- [RE-AUDIT-3X-AFTER.md](./RE-AUDIT-3X-AFTER.md) — live ≥3× after metrics (2026-10-29)
- [evidence/after_3x_metrics.json](./evidence/after_3x_metrics.json)

## Completion layer (anti half-done)

- [docs/COMPLETION-CONTRACT.md](./docs/COMPLETION-CONTRACT.md)
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- scripts/durable_hygiene.py — checkpointed PR/branch hygiene
- scripts/pre_merge_compile_gate.py — stop SyntaxError merges
- Workflow: Completion Hygiene (weekly report; dispatch apply)
