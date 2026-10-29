# Completion Contract (merge / branch / file) — no half-done work

**Status vocabulary:** `RUNNING` | `PARTIAL` | `BLOCKED` | `VERIFIED`  
**Capability hard rule:** do not tighten Actions allow-list, SHA pin, or required human reviews.

## Why work dies halfway

Observed failure modes (2026-10-29 reverse-engineering):

1. **Mutate-then-silence** — scripts only print at the end → look hung → get killed → queue half-applied.
2. **No checkpoint** — kill loses progress; retry double-closes or skips.
3. **Search API for private queue** — hangs / 403 → draft closer never finishes.
4. **Patch without compile gate** — merge lands `SyntaxError` on main (closeout).
5. **Zombie ready PRs** — months-old open non-drafts create merge/branch chaos.
6. **Claim without read-back** — configured ≠ runtime; proof gate fails.

## Contract (agents + humans)

### A. File change
1. Write/edit one atomic concern.
2. **Immediate same-path read-back** (content markers or sha256).
3. If tool says success but fingerprint unchanged → treat as **idempotent**; verify expected markers (do not rewrite to fake a hash delta).
4. Critical Python on default branch: `compile()` before merge.

### B. Branch
1. Never delete: default branch, `release/*`, `hotfix/*`, open-PR heads.
2. Delete only: merged heads **or** stale (>14d) with checkpoint every 25 deletes.
3. Progress log each delete; resume from checkpoint file.

### C. Merge / PR
1. One PR = one concern; either **merge** or **close with reason** — no zombie `ready` forever.
2. Abandoned ready PR: `updated < now-30d` → close `not_planned` + comment (do not merge blindly).
3. Active drafts (updated ≤30d) stay unless author asks.
4. After merge: wait for owning workflow receipt (closeout/compile) before claiming done.

### D. Session durability
1. Use `scripts/durable_hygiene.py` (this repo) for queue/branch ops.
2. Checkpoint path: `evidence/hygiene-checkpoint-<repo>.json`.
3. Kill/resume must continue from checkpoint file — never restart from zero after partial apply.
4. Prefer REST pagination over Search API for private org repos.

## Receipt schema

See `schemas/completion-receipt.schema.json`. Every apply run must emit a receipt under `evidence/`.
