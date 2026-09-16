#!/usr/bin/env python3
"""Refresh data/bnetdocs.json: who wrote each BNETDocs packet page, for credit on our pages.

Only credit metadata is kept (page link, packet name and direction, author, dates, edit
count). BNETDocs' packet formats and remarks are never copied into this site.

Run from anywhere:  python3 scripts/bnetdocs_credits.py
"""
import html
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://bnetdocs.org"
HEADERS = {"User-Agent": "docs.bnet.cc credits refresh (https://github.com/tagban/bnetcc-docs)"}
DIRECTIONS = {1: "c2s", 2: "s2c", 3: "p2p"}


def get_json(path):
    with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=HEADERS), timeout=60) as r:
        return json.load(r)


def credits_page_people():
    """Everyone BNETDocs' credits page links to (documents, comments, packets, servers)."""
    req = urllib.request.Request(BASE + "/credits", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        page = r.read().decode("utf-8", "replace")
    people = {}
    for user_id, name in re.findall(r'href="[^"]*/user/(\d+)[^"]*"[^>]*>(.*?)</a>', page, re.S):
        name = html.unescape(re.sub(r"<[^>]+>", "", name)).strip()
        if name:
            people.setdefault(int(user_id), {"name": name, "url": f"{BASE}/user/{user_id}"})
    return people


def main():
    packets = get_json("/packet/index.json")["packets"]
    names = {}
    for user_id in sorted({p["user_id"] for p in packets if p["user_id"]}):
        user = get_json(f"/user/{user_id}.json")["user"]
        names[user_id] = {"name": user["name"], "url": user["url"]}
        time.sleep(0.5)  # be gentle with BNETDocs

    out = {}
    for p in sorted(packets, key=lambda p: (p["packet_name"], p["packet_direction_id"])):
        entry = {
            "bnetdocs_id": p["id"],
            "url": f"{BASE}/packet/{p['id']}",
            "message_id": f"0x{p['packet_id']:02X}",
            "created": p["created_datetime"]["iso"] if p["created_datetime"] else None,
            "edited": p["edited_datetime"]["iso"] if p["edited_datetime"] else None,
            "edits": p["edited_count"],
            "author": names.get(p["user_id"]),
        }
        out.setdefault(p["packet_name"], {})[DIRECTIONS.get(p["packet_direction_id"], str(p["packet_direction_id"]))] = entry

    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/bnetdocs.json").write_text(json.dumps({
        "source": f"{BASE}/packet/index.json",
        "credits_page": f"{BASE}/credits",
        "authors": sorted(names.values(), key=lambda a: a["name"].lower()),
        "contributors": sorted(
            {**credits_page_people(), **names}.values(), key=lambda a: a["name"].lower()
        ),
        "packets": out,
    }, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(packets)} BNETDocs packet pages, {len(names)} named authors")


if __name__ == "__main__":
    main()
