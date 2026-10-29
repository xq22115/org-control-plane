# Strengthen pass — better than Enterprise leftovers (2026-10-29)

Goal: raise every `xq22115` surface without blind-copying expired Enterprise locks, and without blocking GPT/agent automation.

## Practitioner patterns adapted (solo, no extra model API)

1. **GitHub Docs / plan FAQ** — Free org cannot enforce private rulesets; move enforceable gates to Pro or keep policy-as-code. Soft public rulesets still raise integrity.
2. **Jesse Vincent / Superpowers style** — clarify goal before repair; here: automation-first + evidence PR template before inventing review theater.
3. **Simon Willison agentic engineering** — verify with running checks (`ci-health` smoke + Dependabot), not settings theater alone.

## Applied upgrades vs prior Enterprise residue

| Area | Before (post-expiry) | After strengthen |
|---|---|---|
| Org profile | empty name/description | Named + blog → control plane |
| Repo metadata | empty topics/homepages | Topics + homepage on all |
| Merge hygiene | uneven | squash/rebase, delete branch, no merge commit, wiki/projects off |
| Public integrity | none / soft-only | deletion + non-FF + **linear history**, 0 reviews |
| Secret scanning (public) | basic | + push protection (+ validity where allowed) |
| Thin repos | bare | Dependabot, CODEOWNERS, PR/Issue templates, `ci-health`, AGENTS.md |
| Labels | sparse | shared automation/gate/deps set on all |
| Control plane | private, unprotected | **public** + ruleset + Actions health |

## Still plan-blocked (not ignored — explicit)

- Private rulesets / classic branch protection on Free org private repos
- Org-wide rulesets (Team+)
- Secret scanning non-provider / validity on some surfaces may stay disabled by plan

## Repos in scope

braintrust, cursor, demo-repository, vercel-ai-foundation-e2e-canary, ai-thinking-debate-skills-lab, repo-rescue-proof, org-control-plane
