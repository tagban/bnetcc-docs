---
title: "Warcraft III: logon to chat"
layout: "sequence"
categories: ["Sequences"]
products: [WAR3, W3XP]
summary: "How *Warcraft III* connects, passes the version check, logs on with NLS and joins a channel. Checked against a real *The Frozen Throne* 1.27b client."
bnetdocs_documents: [10, 24]
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_AUTH_INFO, note: "Names the game (`WAR3` or `W3XP`) and version byte (`0x1B` for 1.27b).", confidence: verified }
  - { from: server, packet: SID_PING, confidence: verified }
  - { from: server, packet: SID_AUTH_INFO, note: "Logon type `0x02` (NLS), the version check, and the **128-byte signature**, which must be present.", confidence: verified }
  - { from: client, packet: SID_AUTH_CHECK, note: "*The Frozen Throne* sends two CD keys.", confidence: verified }
  - { from: server, packet: SID_AUTH_CHECK, confidence: verified }
  - { section: "Files, downloaded over BNFTP version 2 on separate connections" }
  - { from: client, packet: SID_GETFILETIME, optional: true, note: "Terms of service and `bnserver-WAR3.ini`, one request each.", confidence: verified }
  - { from: server, packet: SID_GETFILETIME, optional: true, confidence: verified }
  - { from: client, packet: SID_GETICONDATA, confidence: verified }
  - { from: server, packet: SID_GETICONDATA, note: "Usually `icons-WAR3.bni`.", confidence: verified }
  - { section: "Only when the player creates a new account" }
  - { from: client, packet: SID_AUTH_ACCOUNTCREATE, optional: true, note: "Salt and verifier.", confidence: verified }
  - { from: server, packet: SID_AUTH_ACCOUNTCREATE, optional: true, note: "`0x00` created.", confidence: verified }
  - { section: "Logging on" }
  - { from: client, packet: SID_AUTH_ACCOUNTLOGON, note: "Client public key A.", confidence: verified }
  - { from: server, packet: SID_AUTH_ACCOUNTLOGON, note: "Salt and server public key B. Always 72 bytes.", confidence: verified }
  - { from: client, packet: SID_AUTH_ACCOUNTLOGONPROOF, note: "Client proof M1.", confidence: verified }
  - { from: server, packet: SID_AUTH_ACCOUNTLOGONPROOF, note: "Status and server proof M2: **exactly 24 bytes**.", confidence: verified }
  - { section: "Entering chat" }
  - { from: client, packet: SID_NETGAMEPORT, note: "The port it hosts games on.", confidence: verified }
  - { from: client, packet: SID_ENTERCHAT, confidence: verified }
  - { from: server, packet: SID_ENTERCHAT, note: "The client accepts a realm-style name such as `Name@Realm`.", confidence: verified }
  - { from: client, packet: SID_WARCRAFTGENERAL, optional: true, note: "Tournament status and the ladder map list.", confidence: verified }
  - { from: server, packet: SID_WARCRAFTGENERAL, optional: true, confidence: verified }
  - { from: client, packet: SID_FRIENDSLIST, optional: true, confidence: verified }
  - { from: server, packet: SID_FRIENDSLIST, optional: true, confidence: verified }
  - { from: client, packet: SID_NEWS_INFO, optional: true, confidence: verified }
  - { from: server, packet: SID_NEWS_INFO, optional: true, confidence: verified }
  - { from: client, packet: SID_JOINCHANNEL, note: "Flags `0x01` (first join).", confidence: verified }
  - { from: server, packet: SID_CHATEVENT, confidence: verified }
sources:
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "observed from a real Warcraft III: The Frozen Throne 1.27b client on September 11, 2026"
---

**Only NLS works.** An unmodified *Warcraft III* won't use the older X-SHA-1 logon: if the server offers logon type `0x00`, the client disconnects before the version check.

**The server signature.** Under NLS, *Warcraft III* checks the 128-byte signature in `SID_AUTH_INFO` against a key built into the game. No server other than Blizzard's can produce a valid one, so connecting to any other server requires a client modification that skips the check. This site doesn't host or link one. The server simply has to include the 128 bytes; zeros are fine.

**If the client disconnects right after logging on** ("connection to Battle.net has been lost"), check that the `SID_AUTH_ACCOUNTLOGONPROOF` reply is exactly 24 bytes.
