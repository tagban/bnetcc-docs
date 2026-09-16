#!/usr/bin/env python3
"""One-time seed of data/servers.yaml from BNETDocs' server list, with credit.

Keeps each server's name, address, port and type, plus a link to its BNETDocs entry
and who added it. After seeding, edit data/servers.yaml directly.
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://bnetdocs.org"
HEADERS = {"User-Agent": "docs.bnet.cc server list seed (https://github.com/tagban/bnetcc-docs)"}

# BNETDocs server type -> (our group key, how to check it)
TYPES = {
    1: ("websites", "http"), 2: ("websites", "http"), 100: ("websites", "http"),
    10: ("classic-blizzard", "tcp"), 11: ("classic-blizzard", "tcp"),
    12: ("classic-community", "tcp"), 13: ("classic-community", "tcp"),
    20: ("bnls", "tcp"), 21: ("botnet", "tcp"),
    30: ("remastered", "tcp"), 31: ("remastered", "tcp"),
    40: ("bnet2", "tcp"), 41: ("bnet2", "tcp"), 42: ("bnet2", "tcp"),
    43: ("bnet2", "tcp"), 44: ("bnet2", "tcp"), 45: ("bnet2", "tcp"),
}


def get_json(path):
    with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=HEADERS), timeout=60) as r:
        return json.load(r)


def q(value):
    return json.dumps(value, ensure_ascii=False)


def main():
    data = get_json("/servers.json")
    type_labels = {t["id"]: t["label"] for t in data["server_types"]}
    users = {}
    for uid in {s["user_id"] for s in data["servers"] if s["user_id"]}:
        u = get_json(f"/user/{uid}.json")["user"]
        users[uid] = u["name"]

    lines = [
        "# Battle.net servers checked once a day by .github/workflows/server-status.yml.",
        "# Seeded from BNETDocs' server list (credited per entry). Add or edit entries freely.",
        "# check: http (web request) or tcp (can a connection be opened). enabled: false skips a server.",
        "",
    ]
    for s in sorted(data["servers"], key=lambda s: (s["type_id"], s["label"].lower())):
        group, check = TYPES.get(s["type_id"], ("other", "tcp"))
        lines.append(f"- id: {q('bnetdocs-' + str(s['id']))}")
        lines.append(f"  name: {q(s['label'])}")
        lines.append(f"  address: {q(s['address'])}")
        lines.append(f"  port: {s['port']}")
        lines.append(f"  group: {q(group)}")
        lines.append(f"  kind: {q(type_labels.get(s['type_id'], ''))}")
        lines.append(f"  check: {q(check)}")
        if s["status_bitmask"] & 2:
            lines.append("  enabled: false")
        lines.append(f"  bnetdocs: {q(s['uri'])}")
        if s["user_id"]:
            lines.append(f"  added_by: {q(users[s['user_id']])}")
        lines.append("")
    (ROOT / "data/servers.yaml").write_text("\n".join(lines))
    print(f"wrote {len(data['servers'])} servers")


if __name__ == "__main__":
    main()
