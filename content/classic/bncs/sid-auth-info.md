---
title: "SID_AUTH_INFO"
layout: "packet"
protocol: "BNCS"
message_id: "0x50"
categories: ["BNCS", "Logon"]
products: [STAR, SEXP, D2DV, D2XP, WAR3, W3XP]
summary: "The client names its game, platform and version. The server replies with a session token and the version check to run."
c2s:
  when: "The first message a client sends after the `0x01` protocol byte."
  fields:
    - { type: "UINT32", name: "Protocol ID", notes: "`0`.", confidence: single }
    - { type: "DWORD", name: "Platform code", notes: "`IX86` for Windows. Four-character codes appear reversed on the wire.", confidence: verified }
    - { type: "DWORD", name: "Product code", notes: "The game, such as `STAR` or `W3XP`.", confidence: verified }
    - { type: "UINT32", name: "Version byte", notes: "Changes with each game patch. The server uses it to choose which version-check files apply.", confidence: verified }
    - { type: "UINT32", name: "Product language", confidence: single }
    - { type: "UINT32", name: "Local IP address", notes: "The client's address as it sees it, which may be a private address behind NAT.", confidence: single }
    - { type: "UINT32", name: "Time zone bias", notes: "Minutes from UTC.", confidence: single }
    - { type: "UINT32", name: "Locale ID", notes: "A Windows locale ID.", confidence: single }
    - { type: "UINT32", name: "Language ID", notes: "A Windows language ID.", confidence: single }
    - { type: "STRING", name: "Country abbreviation", notes: "For example `USA`.", confidence: single }
    - { type: "STRING", name: "Country name", notes: "For example `United States`.", confidence: single }
s2c:
  fields:
    - { type: "UINT32", name: "Logon type", notes: "Which password system the account logon uses. See the table below.", confidence: verified }
    - { type: "UINT32", name: "Server token", notes: "A random value for this session. The client mixes it into its CD-key and password hashes, so they can't be replayed.", confidence: verified }
    - { type: "UINT32", name: "UDP value", notes: "When this is not zero, the client runs its UDP connectivity test. Games keep **Create** and **Join** greyed out until that test succeeds.", confidence: verified }
    - { type: "FILETIME", name: "Version-check file time", notes: "The time of the version-check MPQ, so a client that keeps a cached copy knows whether to download it again.", confidence: verified }
    - { type: "STRING", name: "Version-check file name", notes: "The MPQ that holds the version-check code, such as `ver-IX86-1.mpq`.", confidence: verified }
    - { type: "STRING", name: "Version-check formula", notes: "The instructions the client runs over its game files to produce the EXE hash sent in `SID_AUTH_CHECK`.", confidence: verified }
    - { type: "VOID", name: "Server signature (128 bytes)", notes: "**Warcraft III only.** The client expects these bytes whatever the logon type, and rejects a reply without them.", confidence: verified }
  values:
    - name: "Logon types"
      items:
        - { value: "0x00", meaning: "X-SHA-1 (\"Broken SHA-1\") password hashing. *StarCraft* and *Diablo II*.", confidence: verified }
        - { value: "0x01", meaning: "NLS (New Logon System), version 1.", confidence: single }
        - { value: "0x02", meaning: "NLS version 2. *Warcraft III*.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "reply layout tested with real StarCraft, Diablo II and Warcraft III clients"
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
---

This message starts the modern Classic logon used by *StarCraft* 1.09 and later, *Diablo II* and *Warcraft III*. Older games (*Diablo*, *StarCraft Shareware*, *Warcraft II*) start with `SID_STARTVERSIONING` instead.

**The UDP test.** After this reply the server sends a UDP packet to the client's port 6112. Once that round trip completes, the client can create and join games. A server that sets the UDP value to zero, or never sends the UDP packet, leaves those buttons disabled.

**Warcraft III's signature.** Under NLS, *Warcraft III* checks the 128-byte signature against a key built into the game. Only Blizzard can produce a valid signature, which is why private *Warcraft III* servers need a modified client. This site does not host or link such modifications.
