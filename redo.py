#!/usr/bin/env python3
"""CLI for the leetcode redo list. Keeps redo.json and redo.md in sync."""

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "redo.json"
MD_PATH = ROOT / "redo.md"

VALID_REASONS = ("fail", "slow", "fumble")
VALID_STATUSES = ("open", "cleared")


def load():
    with open(JSON_PATH) as f:
        return json.load(f)


def save(data):
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def regenerate_md(data):
    rows = []
    open_items = [p for p in data["problems"] if p["status"] == "open"]
    cleared_items = [p for p in data["problems"] if p["status"] == "cleared"]
    for p in open_items + cleared_items:
        rows.append(
            f"| {p['id']} | {p['name']} | {p['pattern']} | {p['added']} "
            f"| {p['reason']} | {p['target_min']}m | {p['status']} "
            f"| {p['last_attempt']} | {p.get('notes', '')} |"
        )
    header = (
        "# Redo List\n\n"
        "| # | name | pattern | added | reason | target | status | last attempt | notes |\n"
        "|---|------|---------|-------|--------|--------|--------|--------------|-------|\n"
    )
    body = "\n".join(rows)
    footer = "\n\n*Auto-generated from redo.json — do not edit by hand.*\n"
    with open(MD_PATH, "w") as f:
        f.write(header + body + footer)


def git_push(message):
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if result.returncode == 0:
        print("No changes to commit.")
        return
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def find_problem(data, pid):
    for p in data["problems"]:
        if p["id"] == pid:
            return p
    return None


def cmd_add(args):
    data = load()
    today = date.today().isoformat()
    existing = find_problem(data, args.id)
    if existing:
        existing["status"] = "open"
        existing["last_attempt"] = today
        if args.notes:
            existing["notes"] = args.notes
        if args.pattern:
            existing["pattern"] = args.pattern
        if args.reason:
            existing["reason"] = args.reason
        if args.target:
            existing["target_min"] = args.target
        print(f"Reopened existing #{args.id} and bumped last_attempt.")
    else:
        entry = {
            "id": args.id,
            "name": args.name,
            "pattern": args.pattern or "",
            "added": today,
            "reason": args.reason or "fail",
            "target_min": args.target or 20,
            "status": "open",
            "last_attempt": today,
            "notes": args.notes or "",
        }
        data["problems"].append(entry)
        print(f"Added #{args.id} {args.name}.")
    save(data)
    regenerate_md(data)
    if not args.no_push:
        git_push(f"add {args.id}")


def cmd_done(args):
    data = load()
    p = find_problem(data, args.id)
    if not p:
        sys.exit(f"Problem #{args.id} not found.")
    p["status"] = "cleared"
    p["last_attempt"] = date.today().isoformat()
    save(data)
    regenerate_md(data)
    print(f"Cleared #{args.id} {p['name']}.")
    if not args.no_push:
        git_push(f"done {args.id}")


def cmd_reopen(args):
    data = load()
    p = find_problem(data, args.id)
    if not p:
        sys.exit(f"Problem #{args.id} not found.")
    p["status"] = "open"
    p["last_attempt"] = date.today().isoformat()
    save(data)
    regenerate_md(data)
    print(f"Reopened #{args.id} {p['name']}.")
    if not args.no_push:
        git_push(f"reopen {args.id}")


def cmd_list(args):
    data = load()
    problems = data["problems"]
    if args.open:
        problems = [p for p in problems if p["status"] == "open"]
    if not problems:
        print("No problems.")
        return
    header = f"{'#':>5}  {'name':<30} {'pattern':<25} {'added':<12} {'reason':<8} {'target':>6}  {'status':<8} {'last attempt':<12} notes"
    print(header)
    print("-" * len(header))
    open_items = [p for p in problems if p["status"] == "open"]
    cleared_items = [p for p in problems if p["status"] == "cleared"]
    for p in open_items + cleared_items:
        print(
            f"{p['id']:>5}  {p['name']:<30} {p['pattern']:<25} {p['added']:<12} "
            f"{p['reason']:<8} {p['target_min']:>4}m  {p['status']:<8} "
            f"{p['last_attempt']:<12} {p.get('notes', '')}"
        )


def main():
    parser = argparse.ArgumentParser(prog="redo", description="LeetCode redo list CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("id", type=int)
    p_add.add_argument("name", type=str)
    p_add.add_argument("--pattern", type=str, default="")
    p_add.add_argument("--reason", type=str, choices=VALID_REASONS, default="fail")
    p_add.add_argument("--target", type=int, default=20)
    p_add.add_argument("--notes", type=str, default="")
    p_add.add_argument("--no-push", action="store_true")
    p_add.set_defaults(func=cmd_add)

    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)
    p_done.add_argument("--no-push", action="store_true")
    p_done.set_defaults(func=cmd_done)

    p_reopen = sub.add_parser("reopen")
    p_reopen.add_argument("id", type=int)
    p_reopen.add_argument("--no-push", action="store_true")
    p_reopen.set_defaults(func=cmd_reopen)

    p_list = sub.add_parser("list")
    p_list.add_argument("--open", action="store_true")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
