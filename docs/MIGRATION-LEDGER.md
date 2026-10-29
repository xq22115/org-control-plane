# Migration ledger — xq22115 Enterprise leftovers → Free+Pro

Status: `VERIFIED` applied | `ADAPTED` changed for Free/Pro | `KEEP` already good | `BLOCKED` needs Team/Pro-on-owner | `SKIP` intentionally not copied

## 1. Org-level controls

| Item | Enterprise-era intent | Free org now | Action | Status |
|---|---|---|---|---|
| Actions allow all | GPT/plugins/workflows free | `allowed_actions=all`, no SHA pin | Keep for automation | KEEP |
| Workflow token write + approve PRs | Agents can write/approve | write + can_approve_pull_request_reviews | Keep | KEEP |
| Default repo permission admin | Full automation | `admin` | Keep (user request) | KEEP |
| Org rulesets | Org-wide main protection | API 403 Team required | Do not fake; Tier B or public soft rulesets | BLOCKED |
| Code security “GitHub recommended” | Dependabot/secret/code scanning | Config id=17 exists; attach-defaults limited | Per-repo Dependabot+vuln enabled | ADAPTED |
| Teams / Projects / OIDC custom sub | Enterprise org shape | 0 teams; no OIDC sub template | Skip empty Enterprise shape | SKIP |
| Webhooks | Integrations | 0 hooks | None to migrate | KEEP |
| GitHub App installations | ~11 apps on org | Still installed | Inventory only; do not reinstall blindly | KEEP |

## 2. Repository placement

| Repo | Visibility | Workflows | Rulesets on Free | Decision |
|---|---|---|---|---|
| `braintrust` | private | ~223 | BLOCKED | **Stay on org** (wired as `xq22115/braintrust`). Enforce via policy-as-code + CI. Transfer to Pro only if willing to rewire consumers. |
| `cursor` | private | ~19 | BLOCKED | Stay; merge defaults applied |
| `demo-repository` | private | ~32 | BLOCKED | Stay (sandbox) |
| `vercel-ai-foundation-e2e-canary` | private | 0 | BLOCKED | Dedup vs `xq22115-pixel/...` — prefer Pro copy for enforceable gates |
| `ai-thinking-debate-skills-lab` | public | ~29 | Soft ruleset applied | Public brand lab |
| `repo-rescue-proof` | public | ~35 | Soft ruleset applied | Public proof |

## 3. Per-repo settings migrated (ADAPTED) — 2026-10-29

- allow_auto_merge=true
- squash+rebase on, merge commit off
- allow_update_branch=true, delete_branch_on_merge=true
- has_wiki=false
- vulnerability alerts + Dependabot security updates ON
- Public only: ruleset `xq22115-soft-main-integrity` (deletion + non_fast_forward)

## 4. Intentionally NOT migrated

- Enterprise-style required reviews / merge queue on private Free org repos
- Cloning all 223 braintrust workflows into every repo
- Org rulesets
- Paying for Team/Enterprise in this pass

## 5. Next levers (user choice)

1. Upgrade org to Team → private rulesets without renaming braintrust
2. Transfer selected private repos to `xq22115-pixel` → rewire remotes/MCP/ChatGPT
3. Keep as-is → Free org automation-first; governance = CI + policy YAML (default)
