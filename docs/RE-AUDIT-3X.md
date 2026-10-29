# Reverse-engineering audit + 3x lift (2026-10-29)

## Definition of ≥3x (no capability downgrade)

| Metric | Before (this session baseline) | Target (≥3x) | Status |
|---|---|---|---|
| Post-Merge red noise | ~12 failing redispatches / few hours on stale SHAs | ≤1 stale fail / day | Fix PR https://github.com/xq22115/braintrust/pull/923 |
| Merged-branch residue | demo 94 / ai-lab 100 page1 branches | ≤1/3 residue | deleted demo=23 ai-lab=38 |
| Governance coverage (thin repos) | near-zero templates | Dependabot+CODEOWNERS+PR/Issue+ci-health | Done prior pass |
| Org discoverability | empty profile/topics | profile+topics+homepage all repos | Done |
| Failure signal quality | failures mixed with chronic stale | only fresh/actionable | In progress via closeout bound |

Capability preserved: Actions=all, admin default, 0 required reviews, GPT plugin path untouched.

## Critical findings (missed earlier)

- **P1** `org.rulesets`: Org rulesets unavailable on Free plan
- **P2** `org.actions`: Actions allow all + no SHA pin — max automation but supply-chain soft
- **P2** `xq22115/ai-thinking-debate-skills-lab`: High branch count (100) — merge hygiene leak
- **P2** `xq22115/braintrust`: High branch count (100) — merge hygiene leak
- **P1** `xq22115/braintrust`: required-checks.yml names may not match active workflow names
- **P2** `xq22115/braintrust`: pull_request_target present — verify untrusted checkout
- **P2** `xq22115/braintrust`: pull_request_target present — verify untrusted checkout
- **P2** `xq22115/braintrust`: pull_request_target present — verify untrusted checkout
- **P2** `xq22115/demo-repository`: High branch count (94) — merge hygiene leak
- **P2** `xq22115/demo-repository`: pull_request_target present — verify untrusted checkout
- **P2** `merge`: allow_auto_merge still false
- **P1** `actions.permissions`: workflows with write-all permissions
- **P1** `duplication`: Duplicate vercel canary on org and personal Pro
- **P1** `xq22115/braintrust`: agent-core-policy enforcement is advisory — Free org cannot activate protect-main ruleset


## Root cause: Post-Merge thrash

Hourly schedule audit SUCCEEDS, then redispatches `workflow_dispatch` with ancient `merge_sha` (e.g. PR #645). Receipt:

- `MISSING_EXACT_SHA_RUN` (ChatGPT GitHub Readiness never ran for that SHA)
- `MISSING_DEPLOYMENT_FOR_SHA`
- `state=BLOCKED` → reselected forever because `reconcile_states` included `BLOCKED` without age/terminal bounds

## Fix shipped

- PR: https://github.com/xq22115/braintrust/pull/923
- Bound `reconcile_max_age_days=14` + terminal classification skip when stale
- Branch hygiene deletes on merged same-repo heads

## Metrics snapshot from RE audit

```json
{
  "repo_count": 7,
  "github_apps": 11,
  "workflow_total_listed": 346,
  "recent_failure_runs_sampled": 50,
  "open_dependabot_alert_samples": 5,
  "write_all_workflow_hits": 6,
  "required_check_mismatch_repos": 1,
  "findings_by_sev": {
    "P1": 5,
    "P2": 9
  }
}
```

## Apps on org (kept)

```json
[
  {
    "app": "linear-code",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "deployments",
      "merge_queues",
      "pull_requests"
    ]
  },
  {
    "app": "chatgpt-codex-connector",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "pull_requests"
    ]
  },
  {
    "app": "cursor",
    "repos": "all",
    "perms": [
      "pages",
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "packages",
      "statuses",
      "workflows",
      "deployments",
      "discussions",
      "merge_queues",
      "pull_requests",
      "administration",
      "organization_custom_roles",
      "organization_custom_org_roles",
      "organization_custom_properties"
    ]
  },
  {
    "app": "codacy-production",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "members",
      "contents",
      "metadata",
      "statuses",
      "merge_queues",
      "pull_requests",
      "repository_hooks",
      "organization_hooks",
      "repository_custom_properties",
      "organization_custom_properties"
    ]
  },
  {
    "app": "render",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "deployments",
      "environments",
      "pull_requests",
      "repository_hooks",
      "vulnerability_alerts"
    ]
  },
  {
    "app": "openhands-ai",
    "repos": "all",
    "perms": [
      "issues",
      "actions",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "pull_requests",
      "repository_hooks"
    ]
  },
  {
    "app": "coderabbitai",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "statuses",
      "discussions",
      "merge_queues",
      "pull_requests"
    ]
  },
  {
    "app": "notion-ai-connector",
    "repos": "all",
    "perms": [
      "issues",
      "members",
      "contents",
      "metadata",
      "pull_requests",
      "administration",
      "organization_plan"
    ]
  },
  {
    "app": "buildkite",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "packages",
      "statuses",
      "deployments",
      "attestations",
      "environments",
      "pull_requests",
      "repository_hooks",
      "actions_variables",
      "artifact_metadata"
    ]
  },
  {
    "app": "vercel",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "deployments",
      "pull_requests",
      "administration",
      "repository_hooks"
    ]
  },
  {
    "app": "grok-by-xai",
    "repos": "all",
    "perms": [
      "checks",
      "issues",
      "actions",
      "members",
      "contents",
      "metadata",
      "statuses",
      "workflows",
      "discussions",
      "pull_requests",
      "administration",
      "security_events",
      "repository_projects",
      "vulnerability_alerts",
      "secret_scanning_alerts"
    ]
  }
]
```
