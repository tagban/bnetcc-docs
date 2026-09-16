---
title: "SID_AUTH_CHECK"
layout: "packet"
protocol: "BNCS"
message_id: "0x51"
categories: ["BNCS", "Logon"]
products: [STAR, SEXP, D2DV, D2XP, WAR3, W3XP]
summary: "The client proves its game version and CD keys. The server accepts or rejects them."
c2s:
  when: "After the server's `SID_AUTH_INFO`, once the client has run the version check."
  fields:
    - { type: "UINT32", name: "Client token", notes: "A random value chosen by the client for this session.", confidence: verified }
    - { type: "UINT32", name: "EXE version", notes: "The game executable's version.", confidence: verified }
    - { type: "UINT32", name: "EXE hash", notes: "The result of running the version-check formula over the game files.", confidence: verified }
    - { type: "UINT32", name: "Number of CD keys", notes: "`1` for most games. `2` for expansions that also need the original game's key.", confidence: verified }
    - { type: "UINT32", name: "Spawn", notes: "`1` for a spawned (limited) installation, otherwise `0`.", confidence: verified }
    - repeat: "For each CD key"
      fields:
        - { type: "UINT32", name: "Key length", notes: "Number of characters in the key.", confidence: verified }
        - { type: "UINT32", name: "Product value", notes: "Decoded from the key.", confidence: verified }
        - { type: "UINT32", name: "Public value", notes: "Decoded from the key.", confidence: verified }
        - { type: "UINT32", name: "Unused", notes: "`0`.", confidence: verified }
        - { type: "VOID", name: "Key hash (20 bytes)", notes: "Mixed with both tokens, so it is **different every session**. It cannot identify a key; use the product and public values for that.", confidence: verified }
    - { type: "STRING", name: "EXE information", notes: "The executable's name, date and size.", confidence: verified }
    - { type: "STRING", name: "Key owner", notes: "The name entered when the game was installed.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", notes: "See the table below.", confidence: verified }
    - { type: "STRING", name: "Additional information", notes: "Depends on the result: a patch file name for an old version, or who is using a key.", confidence: single }
  values:
    - name: "Results"
      items:
        - { value: "0x000", meaning: "Passed. The client continues to the account logon.", confidence: verified }
        - { value: "0x100", meaning: "Game version too old. The additional information names a patch MPQ, and the client shows an upgrade message.", confidence: verified }
        - { value: "0x101", meaning: "Game version not valid.", confidence: single }
        - { value: "0x102", meaning: "Game version too new.", confidence: single }
        - { value: "0x200", meaning: "CD key not valid.", confidence: single }
        - { value: "0x201", meaning: "CD key already in use. The additional information names who is using it.", confidence: single }
        - { value: "0x202", meaning: "CD key banned.", confidence: single }
        - { value: "0x203", meaning: "CD key is for a different game.", confidence: single }
        - { value: "0x210 – 0x213", meaning: "The same four key problems (not valid, in use, banned, wrong game), for the expansion's key.", confidence: single }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "request layout captured from a real client on September 9, 2026"
---

**Where the CD-key block goes.** The per-key block comes **before** the EXE information string. This order was confirmed from a real client's single-key logon. The two-key layout used by expansions follows the same pattern but hasn't been captured yet.

**Recognising a key.** Because the key hash changes every session, a server that wants to allow only one session per CD key has to compare the product and public values instead.
