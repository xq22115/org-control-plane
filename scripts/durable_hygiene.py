#!/usr/bin/env python3
"""Durable PR/branch hygiene: progress + checkpoint + resume (no half-apply)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote

CHECKPOINT_EVERY = 25
PROTECTED_EXACT = {"main", "master", "develop", "gh-pages"}
PROTECTED_PREFIXES = ("release/", "hotfix/")


def gh(method: str, path: str, data=None):
    args = ["gh", "api", "-X", method, path]
    if data is None:
        r = subprocess.run(args, capture_output=True, text=True)
    else:
        r = subprocess.run(
            args + ["--input", "-"],
            input=json.dumps(data),
            capture_output=True,
            text=True,
        )
    body = None
    if r.stdout.strip():
        try:
            body = json.loads(r.stdout)
        except Exception:
            body = r.stdout
    return r.returncode, body, r.stderr


def log(msg: str) -> None:
    print(msg, flush=True)


def load_checkpoint(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {
        "schema_version": 1,
        "closed_prs": [],
        "deleted_branches": [],
        "failed": [],
        "started_at": datetime.now(timezone.utc).isoformat(),
    }


def save_checkpoint(path: Path, cp: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cp["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(cp, indent=2) + "\n")
    log(
        "CHECKPOINT written %s closed=%s deleted=%s"
        % (path, len(cp["closed_prs"]), len(cp["deleted_branches"]))
    )


def list_open_pulls(repo: str) -> list:
    out = []
    page = 1
    while page <= 30:
        code, body, err = gh(
            "GET", "repos/%s/pulls?state=open&per_page=100&page=%s" % (repo, page)
        )
        if code != 0:
            raise SystemExit("list pulls failed: %s" % err)
        if not body:
            break
        out.extend(body)
        log("progress pulls_page=%s batch=%s total=%s" % (page, len(body), len(out)))
        if len(body) < 100:
            break
        page += 1
    return out


def list_branches_dated(repo: str) -> list:
    q = (
        "query($owner:String!, $name:String!, $after:String) {"
        " repository(owner:$owner, name:$name) {"
        '  refs(refPrefix:"refs/heads/", first:100, after:$after) {'
        "   pageInfo { hasNextPage endCursor }"
        "   nodes { name target { ... on Commit { committedDate } } }"
        "  } } }"
    )
    owner, name = repo.split("/", 1)
    after = None
    out = []
    for page in range(1, 41):
        code, body, err = gh(
            "POST",
            "graphql",
            {"query": q, "variables": {"owner": owner, "name": name, "after": after}},
        )
        if code != 0 or (isinstance(body, dict) and body.get("errors")):
            raise SystemExit(err or body)
        refs = body["data"]["repository"]["refs"]
        for n in refs["nodes"]:
            tgt = n.get("target") or {}
            out.append({"name": n["name"], "date": tgt.get("committedDate")})
        log("progress branches_page=%s total=%s" % (page, len(out)))
        if not refs["pageInfo"]["hasNextPage"]:
            break
        after = refs["pageInfo"]["endCursor"]
    return out


def close_abandoned_ready(repo, days, mode, cp, cp_path):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    done = set(cp.get("closed_prs") or [])
    pulls = list_open_pulls(repo)
    closed = 0
    for p in pulls:
        n = p["number"]
        if n in done or p.get("draft"):
            continue
        updated = datetime.fromisoformat(p["updated_at"].replace("Z", "+00:00"))
        if updated >= cutoff:
            continue
        log("candidate close PR #%s updated=%s" % (n, p["updated_at"]))
        if mode != "apply":
            closed += 1
            continue
        comment = (
            "Closing as **abandoned ready PR** under Completion Contract "
            "(no update since %s, threshold %sd). "
            "Re-open if still needed — active drafts untouched."
            % (p["updated_at"][:10], days)
        )
        gh("POST", "repos/%s/issues/%s/comments" % (repo, n), {"body": comment})
        code, _, err = gh("PATCH", "repos/%s/pulls/%s" % (repo, n), {"state": "closed"})
        if code != 0:
            gh(
                "PATCH",
                "repos/%s/issues/%s" % (repo, n),
                {"state": "closed", "state_reason": "not_planned"},
            )
        _, body, _ = gh("GET", "repos/%s/pulls/%s" % (repo, n))
        state = (body or {}).get("state") if isinstance(body, dict) else None
        if state != "closed":
            cp.setdefault("failed", []).append({"pr": n, "err": str(err)[-120:]})
            log("FAIL close PR #%s state=%s" % (n, state))
            continue
        cp["closed_prs"].append(n)
        closed += 1
        log("OK closed PR #%s" % n)
        if closed % CHECKPOINT_EVERY == 0:
            save_checkpoint(cp_path, cp)
        time.sleep(0.12)
    return closed


def purge_branches(repo, keep_days, mode, cp, cp_path):
    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    done = set(cp.get("deleted_branches") or [])
    open_heads = {p["head"]["ref"] for p in list_open_pulls(repo)}
    merged = set()
    for page in range(1, 4):
        code, body, _ = gh(
            "GET",
            "repos/%s/pulls?state=closed&per_page=100&page=%s&sort=updated&direction=desc"
            % (repo, page),
        )
        if code != 0 or not body:
            break
        for p in body:
            if p.get("merged_at"):
                merged.add(p["head"]["ref"])
    branches = list_branches_dated(repo)
    deleted = 0
    for b in branches:
        name = b["name"]
        if name in done:
            continue
        if name in PROTECTED_EXACT or any(name.startswith(pfx) for pfx in PROTECTED_PREFIXES):
            continue
        if name in open_heads:
            continue
        date_s = b.get("date")
        if not date_s:
            continue
        dt = datetime.fromisoformat(date_s.replace("Z", "+00:00"))
        if name not in merged and dt >= cutoff:
            continue
        reason = "merged" if name in merged else "stale"
        log("candidate delete branch=%s reason=%s" % (name, reason))
        if mode != "apply":
            deleted += 1
            continue
        ref = quote(name, safe="")
        code, _, err = gh("DELETE", "repos/%s/git/refs/heads/%s" % (repo, ref))
        if code != 0:
            cp.setdefault("failed", []).append({"branch": name, "err": str(err)[-120:]})
            log("FAIL delete %s" % name)
            continue
        cp["deleted_branches"].append(name)
        deleted += 1
        log("OK deleted %s" % name)
        if deleted % CHECKPOINT_EVERY == 0:
            save_checkpoint(cp_path, cp)
        time.sleep(0.03)
    return deleted


def readback(repo: str) -> dict:
    owner, name = repo.split("/", 1)
    q = (
        'query { r: repository(owner:"%s", name:"%s") '
        '{ refs(refPrefix:"refs/heads/", first:1) { totalCount } '
        "pullRequests(states:OPEN) { totalCount } } }" % (owner, name)
    )
    code, body, err = gh("POST", "graphql", {"query": q})
    if code != 0:
        return {"error": err}
    node = body["data"]["r"]
    return {
        "open_prs": node["pullRequests"]["totalCount"],
        "branches": node["refs"]["totalCount"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--mode", choices=["report", "apply"], default="report")
    ap.add_argument("--abandon-days", type=int, default=30)
    ap.add_argument("--branch-keep-days", type=int, default=14)
    ap.add_argument("--skip-prs", action="store_true")
    ap.add_argument("--skip-branches", action="store_true")
    ap.add_argument("--checkpoint", default="")
    ap.add_argument("--receipt", default="")
    args = ap.parse_args()

    slug = args.repo.replace("/", "__")
    cp_path = (
        Path(args.checkpoint)
        if args.checkpoint
        else Path("evidence/hygiene-checkpoint-%s.json" % slug)
    )
    cp = load_checkpoint(cp_path)
    log("START repo=%s mode=%s checkpoint=%s" % (args.repo, args.mode, cp_path))
    before = readback(args.repo)
    log("READBACK_BEFORE %s" % json.dumps(before))
    prs = 0
    br = 0
    if not args.skip_prs:
        prs = close_abandoned_ready(args.repo, args.abandon_days, args.mode, cp, cp_path)
    if not args.skip_branches:
        br = purge_branches(args.repo, args.branch_keep_days, args.mode, cp, cp_path)
    save_checkpoint(cp_path, cp)
    after = readback(args.repo)
    log("READBACK_AFTER %s" % json.dumps(after))
    status = "VERIFIED"
    if cp.get("failed"):
        status = "PARTIAL"
    if args.mode == "report":
        status = "PARTIAL"
    receipt = {
        "schema_version": 1,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "repo": args.repo,
        "mode": args.mode,
        "status": status,
        "checkpoint_path": str(cp_path),
        "ops": {
            "prs_closed_or_candidates": prs,
            "branches_deleted_or_candidates": br,
            "failed": len(cp.get("failed") or []),
            "checkpoint_closed_prs": len(cp.get("closed_prs") or []),
            "checkpoint_deleted_branches": len(cp.get("deleted_branches") or []),
        },
        "readback": {"before": before, "after": after},
        "errors": [json.dumps(x) for x in (cp.get("failed") or [])][:20],
    }
    receipt_path = (
        Path(args.receipt)
        if args.receipt
        else Path("evidence/completion-receipt-%s-%s.json" % (slug, args.mode))
    )
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    log("RECEIPT %s status=%s" % (receipt_path, status))
    print(json.dumps(receipt, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
