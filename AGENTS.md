# AGENTS

- Org SSOT / migration: https://github.com/xq22115/org-control-plane
- Primary private control plane: https://github.com/xq22115/braintrust
- Prefer evidence + read-back over claims; keep automation unblocked (0 required human reviews).

## Completion (mandatory)

1. Read `docs/COMPLETION-CONTRACT.md` before merge / branch delete / bulk file ops.
2. Use `scripts/durable_hygiene.py` for queue/branch apply (checkpoint + progress). Never Search API for private org PR lists.
3. Before merging critical Python to default branch: run `pre_merge_compile_gate.py`.
4. Status only: RUNNING / PARTIAL / BLOCKED / VERIFIED — no silent halfway stop.
