#!/usr/bin/env python3
"""Independent owner readback for Render live-channel hardening."""
from __future__ import annotations
import json, subprocess, sys, urllib.request
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

RENDER = "render"

@dataclass(frozen=True)
class Target:
    workspace_id: str
    service_id: str
    expect_health: str
    live_url: str

TARGETS: Tuple[Target, ...] = (
    Target("tea-db40dqeb7d7c739t0ffg", "srv-db40joks728c73fghotg", "/livez", "https://rdc-ws2-windows-20261009.onrender.com/livez"),
    Target("tea-db40dqeb7d7c739t0ffg", "srv-db40jqij9qps73fnb89g", "/livez", "https://rdc-ws2-mac-20261009.onrender.com/livez"),
    Target("tea-db40dqeb7d7c739t0ffg", "srv-db53j3g473hc739oj91g", "/livez", "https://rdc-ws3-mac-20261010.onrender.com/livez"),
    Target("tea-db40dqeb7d7c739t0ffg", "srv-dbhn5n8n74is73egk9sg", "/livez", "https://windows-rdc4-quanmian-nianya-20261030.onrender.com/livez"),
    Target("tea-db40dqeb7d7c739t0ffg", "srv-dber34rrjlhs738jvac0", "/livez", "https://gpt6-codex-test1-ws2-25usd-20261025.onrender.com/livez"),
    Target("tea-db40dqeb7d7c739t0ffg", "srv-dbhjveu7bikc73eqta80", "/healthz", "https://gpt56-model7-account1-secretary-starter.onrender.com/healthz"),
    Target("tea-da1crpjl550s73fcph00", "srv-db23d3jbc2fs73f38clg", "/livez", "https://selfhost-rdc-windows-20261006.onrender.com/livez"),
    Target("tea-da1crpjl550s73fcph00", "srv-db2bdp0ae00c739oav2g", "/livez", "https://cloud-native-56-final-20261006.onrender.com/livez"),
    Target("tea-da1crpjl550s73fcph00", "srv-dbbdukk9v7es73est1e0", "/livez", "https://rdc-ws3-windows-canary-20261020.onrender.com/livez"),
    Target("tea-da1crpjl550s73fcph00", "srv-db1qeqk9v7es738ot720", "/livez", "https://selfhost-rdc-a2-20261005.onrender.com/livez"),
)

def set_workspace(workspace_id: str) -> None:
    subprocess.check_call([RENDER, "workspace", "set", workspace_id, "--confirm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def service_index(workspace_id: str) -> Dict[str, dict]:
    set_workspace(workspace_id)
    payload = json.loads(subprocess.check_output([RENDER, "services", "list", "-o", "json"], text=True))
    out: Dict[str, dict] = {}
    for entry in payload:
        svc = entry.get("service")
        if svc:
            out[svc["id"]] = svc
    return out

def http_status(url: str) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "org-control-plane-render-verify"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        return int(resp.status)

def verify(targets: Iterable[Target] = TARGETS) -> int:
    cache: Dict[str, Dict[str, dict]] = {}
    failures = 0
    target_list = list(targets)
    for t in target_list:
        if t.workspace_id not in cache:
            cache[t.workspace_id] = service_index(t.workspace_id)
        svc = cache[t.workspace_id].get(t.service_id)
        if not svc:
            print(f"FAIL missing {t.service_id}")
            failures += 1
            continue
        details = svc.get("serviceDetails") or {}
        auto = svc.get("autoDeploy")
        health = details.get("healthCheckPath")
        try:
            live = http_status(t.live_url)
        except Exception as exc:
            live = f"ERR:{type(exc).__name__}"
        ok = auto == "yes" and health == t.expect_health and live == 200
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'} {svc.get('name')} ad={auto} hc={health} live={live} br={svc.get('branch')}")
    set_workspace("tea-db40dqeb7d7c739t0ffg")
    print(f"SUMMARY {len(target_list) - failures}/{len(target_list)}")
    return 0 if failures == 0 else 1

if __name__ == "__main__":
    sys.exit(verify())
