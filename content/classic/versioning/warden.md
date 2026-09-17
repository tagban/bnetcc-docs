---
title: "Warden"
categories: ["Classic Battle.net", "Version checking"]
products: [STAR, SEXP, WAR3, W3XP]
summary: "Blizzard's later anti-cheat system for Classic games. It's switched off, so clients, bots and servers can ignore it."
bnetdocs_packets: [SID_WARDEN, BNLS_WARDEN]
sources:
  - name: "iago and Ringo"
    note: "researched the Warden message format, as credited on BNETDocs"
  - name: "BNET.cc operators"
    note: "Warden is off on today's servers; Command Center never sends it"
---

**Warden is off.** Today's Classic servers don't send it, and a client or bot connecting now doesn't need to handle it. There's nothing more to implement, so this site doesn't document it further.

If a server ever sends you `SID_WARDEN`, please tell us on the [BNET.cc Discord](https://discord.gg/dR4djHweh3).

## What it was

Warden was an anti-cheat system Blizzard added to Classic Battle.net after [CheckRevision](/classic/versioning/checkrevision/). A version check runs once, while logging on. Warden kept checking the game while it was connected.

- **Message:** `SID_WARDEN` (`0x5E`), in both directions, sent after logon.
- **Encryption:** RC4, with a different key for each direction.
- **What it did:** the server sent a small program (a "module"), which the client downloaded and ran. The server then asked the module to read parts of the game's memory and report hashes.
- **If you didn't answer:** the server disconnected the client about two minutes later.

Bots handled it with help from BNLS servers (`BNLS_WARDEN`, `0x7D`), which are now also obsolete.

## Server authors

Don't send `SID_WARDEN`. Command Center has no Warden code at all, and clients connect to it without trouble.

This site doesn't document ways around anti-cheat systems.
