# Render fleet hardening — 2026-10-30

## Principle (raise-only, no capability cut)

- Keep working deploy/release branches as the live channel when they diverge from `main`.
- Do not retarget production services to `main` while deploy branches are diverged.
- Strengthen the live channel: `autoDeploy=yes` + verified health path + independent HTTP readback.
- GitHub trunk stays `main`; short-lived PR branches use auto-merge / squash / delete-branch.
- Rulesets that block AI direct-push remain disabled until explicit guarded activation.

## Workspaces

| Workspace | ID | Role |
|---|---|---|
| My Workspace | `tea-da1crpjl550s73fcph00` | selfhost / cloud56 / ws3 canary |
| ai. 2 | `tea-db40dqeb7d7c739t0ffg` | canonical RDC WS2/WS3/WS4 |
| ai3 | `tea-dbbchs5g1s2s738eq430` | spare |

## Hardened live services (owner readback 10/10 PASS)

| Service | Workspace | Health | Auto-deploy | Deploy branch |
|---|---|---|---|---|
| rdc-ws2-windows-20261009 | ai. 2 | `/livez` | yes | `fix/ws2-mcp-resource-compat-20261029` |
| rdc-ws2-mac-20261009 | ai. 2 | `/livez` | yes | `feat/ws2-ack-replay-inbox-20261013` |
| rdc-ws3-mac-20261010 | ai. 2 | `/livez` | yes | `feat/a2-selfhost-rdc-oauth-20261005` |
| windows-rdc4-quanmian-nianya-20261030 | ai. 2 | `/livez` | yes | `deploy/ws4-windows-unified-20261030` |
| gpt6-codex-test1-ws2-25usd-20261025 | ai. 2 | `/livez` | yes | `fix/ws2-windows-native-liveness-20261025` |
| gpt56-model7-account1-secretary-starter | ai. 2 | `/healthz` | yes | `feat/a1-model7-secretary-20261012` |
| selfhost-rdc-a2-20261005 | My Workspace | `/livez` | yes | `feat/a2-selfhost-rdc-oauth-20261005` |
| selfhost-rdc-windows-20261006 | My Workspace | `/livez` | yes | `feat/a2-selfhost-rdc-oauth-20261005` |
| cloud-native-56-final-20261006 | My Workspace | `/livez` | yes | `release/cloud56-final-20261006` |
| rdc-ws3-windows-canary-20261020 | My Workspace | `/livez` | yes | `experiment/ws3-windows-rdc-canary-20261020` |

## GitHub merge plane

Applied to 28 repos under `xq22115-pixel` + `xq22115`: auto-merge, all merge strategies, delete-branch-on-merge, update-branch, vuln alerts + Dependabot. chatgpt-mcp-codex rulesets disabled. Org Actions allowed_actions=all, workflow write.

## Trunk / branch model

main (trunk) receives short-lived PRs. Render serves release/deploy channels until integrate + exact SHA + live health prove a main cutover is safe.

## Consumer proof

- Canonical MCP: https://rdc-ws2-windows-20261009.onrender.com/mcp
- Auth repair: xq22115-pixel gh restored; ~/.gemini/config/github_pat for MCP fallback

## Non-goals

No mass-unsuspend of canaries; no force-merge of diverged deploy branches into main; no paid GHAS private secret scanning.
