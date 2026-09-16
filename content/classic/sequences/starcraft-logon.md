---
title: "StarCraft and Brood War: logon to chat"
layout: "sequence"
categories: ["Sequences"]
products: [STAR, SEXP]
summary: "How *StarCraft* and *Brood War* up to version 1.16.1 connect, pass the version check, log on and join a channel."
bnetdocs_documents: [10]
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_AUTH_INFO, note: "Names the game (`STAR` or `SEXP`), platform and version byte.", confidence: verified }
  - { from: server, packet: SID_PING, note: "Latency check.", confidence: verified }
  - { from: client, packet: SID_PING, optional: true, note: "Echo of the server's value.", confidence: single }
  - { from: server, packet: SID_AUTH_INFO, note: "Logon type `0x00` (X-SHA-1), server token, and the version check to run.", confidence: verified }
  - { from: server, raw: "PKT_SERVERPING", transport: "UDP", note: "UDP test to the client's port 6112.", confidence: verified }
  - { from: client, packet: SID_AUTH_CHECK, note: "EXE hash and one CD key.", confidence: verified }
  - { from: server, packet: SID_AUTH_CHECK, note: "`0x000` when the version and key pass.", confidence: verified }
  - { section: "Optional, in roughly this order: icons, terms of service and profile" }
  - { from: client, raw: "SID_GETICONDATA", optional: true, confidence: single }
  - { from: client, raw: "SID_GETFILETIME", optional: true, note: "For `icons_STAR.bni`.", confidence: single }
  - { from: client, packet: SID_UDPPINGRESPONSE, optional: true, note: "Confirms the UDP test.", confidence: single }
  - { from: server, raw: "SID_GETICONDATA", optional: true, confidence: single }
  - { from: client, raw: "SID_GETFILETIME", optional: true, note: "For `tos_USA.txt`, then `bnserver.ini`.", confidence: single }
  - { from: client, raw: "SID_READUSERDATA", optional: true, confidence: single }
  - { from: server, raw: "SID_GETFILETIME", optional: true, note: "One reply for each request.", confidence: single }
  - { from: server, raw: "SID_READUSERDATA", optional: true, confidence: single }
  - { section: "Only when the player creates a new account" }
  - { from: client, packet: SID_CREATEACCOUNT2, optional: true, note: "Password hashed once.", confidence: verified }
  - { from: server, packet: SID_CREATEACCOUNT2, optional: true, note: "`0x00` created, or `0x04` if the name is taken.", confidence: verified }
  - { section: "Logging on" }
  - { from: client, packet: SID_LOGONRESPONSE2, note: "Salted password proof.", confidence: verified }
  - { from: server, packet: SID_LOGONRESPONSE2, note: "`0x00` logged on.", confidence: verified }
  - { section: "Entering chat" }
  - { from: client, packet: SID_ENTERCHAT, confidence: verified }
  - { from: client, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: client, packet: SID_JOINCHANNEL, note: "Flags `0x01` (first join).", confidence: verified }
  - { from: server, packet: SID_ENTERCHAT, note: "The client's unique name and statstring.", confidence: verified }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: verified }
  - { from: server, packet: SID_CHATEVENT, note: "`EID_CHANNEL`, then `EID_SHOWUSER` for each user in the channel.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling and test client"
    url: "https://github.com/tagban/bnet_command_center/tree/master/crates"
    note: "tested with a real StarCraft 1.16.1 client"
---

**Versions covered.** This sequence is for *StarCraft* and *Brood War* up to 1.16.1. Version 1.18 and later connect differently.

**When `SID_PING` is sent.** Official Battle.net sends `SID_PING` once `SID_AUTH_INFO` arrives. Command Center sends it as soon as the connection opens, and real clients accept that too.

**Brood War 1.16.1** may send `SID_STOPADV` before logon finishes. That's normal and shouldn't be treated as an error.
