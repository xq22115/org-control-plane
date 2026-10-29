# Target architecture (logical) + completion layer

```
ChatGPT / Cursor / Antigravity / gh
            |
            v
   xq22115 (Free org)
   - public labs + soft integrity
   - Actions=all (GPT plugin friendly)
   - braintrust SSOT (policy-as-code)
            |
            |  private enforceable gates?
            v
   xq22115-pixel (Pro)  <-- transfer only when needed
   - rulesets / envs / CODEOWNERS hard

   org-control-plane (this repo)
   - migration ledger + thin templates
   - COMPLETION CONTRACT (merge/branch/file)
   - durable_hygiene.py (checkpoint + resume)
   - pre_merge_compile_gate.py
```

## Completion layer (anti half-done)

| Concern | Owner | Mechanism |
|---|---|---|
| File mutate | Agent | same-path read-back; idempotent OK if markers match |
| Critical Python merge | Agent + CI | pre_merge_compile_gate.py before merge to default |
| PR queue | durable_hygiene.py | close abandoned ready (>30d); keep active drafts |
| Branches | durable_hygiene.py | delete merged/stale; never open-PR/protected; checkpoint/25 |
| Session kill | Checkpoint JSON | resume — do not restart from zero mid-apply |
| Capability | Hard rule | Actions=all, no SHA pin mandate, 0 required human reviews |

See [COMPLETION-CONTRACT.md](./COMPLETION-CONTRACT.md).
