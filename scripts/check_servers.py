#!/usr/bin/env python3
"""Check whether each server in data/servers.yaml is reachable, once a day.

Writes data/server-status.json. The check is deliberately gentle: one TCP connection per
server, closed straight away. No game or logon data is ever sent, so nothing is logged in to.

Usage:  python3 scripts/check_servers.py [--limit N]
"""
import argparse
import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 8


def load_servers():
    """Tiny reader for data/servers.yaml's flat list of '- key: value' records."""
    servers, current = [], None
    for line in (ROOT / "data/servers.yaml").read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(-\s+|\s+)(\w+):\s*(.*)$", line)
        if not m:
            continue
        if m.group(1).startswith("-"):
            current = {}
            servers.append(current)
        value = m.group(3).strip()
        try:
            value = json.loads(value)
        except ValueError:
            pass
        current[m.group(2)] = value
    return servers


def check_tcp(address, port):
    start = time.monotonic()
    with socket.create_connection((address, port), timeout=TIMEOUT):
        return round((time.monotonic() - start) * 1000)


def check(server):
    if server.get("enabled") is False:
        return server["id"], {"checked": False}
    try:
        latency = check_tcp(server["address"], int(server["port"]))
        return server["id"], {"online": True, "latency_ms": latency}
    except Exception as e:  # any failure to connect counts as offline
        reason = type(e).__name__ if not str(e) else str(e)
        return server["id"], {"online": False, "error": reason[:120]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="only check the first N servers (for testing)")
    args = parser.parse_args()

    servers = load_servers()[: args.limit]
    out_path = ROOT / "data/server-status.json"
    previous = json.loads(out_path.read_text())["servers"] if out_path.exists() else {}
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    with ThreadPoolExecutor(max_workers=16) as pool:
        results = dict(pool.map(check, servers))

    status = {}
    for sid, result in results.items():
        before = previous.get(sid, {})
        if result.get("online"):
            result["last_online"] = now
        elif before.get("last_online"):
            result["last_online"] = before["last_online"]
        if before.get("online") == result.get("online") and before.get("since"):
            result["since"] = before["since"]
        else:
            result["since"] = now
        status[sid] = result

    out_path.write_text(json.dumps({"checked": now, "servers": status}, indent=1, sort_keys=True) + "\n")
    online = sum(1 for r in status.values() if r.get("online"))
    print(f"{online} of {len(status)} servers online")


if __name__ == "__main__":
    main()
