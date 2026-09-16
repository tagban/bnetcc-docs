---
title: "StarCraft and Brood War: logon to chat"
layout: "sequence"
categories: ["Sequences"]
products: [STAR, SEXP]
summary: "How *StarCraft* 1.16.1 connects, passes the version check, logs on and joins a channel."
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: server, packet: SID_PING, note: "Sent right away. The client echoes it (step 6), and that round trip is its latency.", confidence: verified }
  - { from: client, packet: SID_AUTH_INFO, note: "Names the game (`STAR` or `SEXP`), platform and version byte.", confidence: verified }
  - { from: server, packet: SID_AUTH_INFO, note: "Logon type `0x00` (X-SHA-1), server token, and the version check to run.", confidence: verified }
  - { from: server, raw: "PKT_SERVERPING", transport: "UDP", note: "UDP test to the client's port 6112. Create and Join stay disabled until it succeeds.", confidence: verified }
  - { from: client, packet: SID_PING, note: "Echo of step 2. Its exact position varies.", confidence: single }
  - { from: client, packet: SID_AUTH_CHECK, note: "EXE hash and one CD key.", confidence: verified }
  - { from: server, packet: SID_AUTH_CHECK, note: "`0x000` when the version and key pass.", confidence: verified }
  - { section: "Only when the player creates a new account" }
  - { from: client, packet: SID_CREATEACCOUNT2, optional: true, note: "Password hashed once.", confidence: verified }
  - { from: server, packet: SID_CREATEACCOUNT2, optional: true, note: "`0x00` created, or `0x04` if the name is taken.", confidence: verified }
  - { section: "Every logon" }
  - { from: client, packet: SID_LOGONRESPONSE2, note: "Salted password proof.", confidence: verified }
  - { from: server, packet: SID_LOGONRESPONSE2, note: "`0x00` logged on.", confidence: verified }
  - { from: client, packet: SID_ENTERCHAT, confidence: verified }
  - { from: server, packet: SID_ENTERCHAT, note: "The client's unique name and statstring.", confidence: verified }
  - { from: client, packet: SID_GETCHANNELLIST, note: "Fills the channel picker. Its exact position varies.", confidence: single }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: verified }
  - { from: client, packet: SID_JOINCHANNEL, note: "Flags `0x01` (first join).", confidence: verified }
  - { from: server, packet: SID_CHATEVENT, note: "`EID_CHANNEL`, then `EID_SHOWUSER` for each user in the channel.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling and test client"
    url: "https://github.com/tagban/bnet_command_center/tree/master/crates"
    note: "tested with a real StarCraft 1.16.1 client"
---

**Not shown yet.** A real *StarCraft* client sends several other messages during logon, such as icon, advertisement and profile requests. They'll be added once their positions are captured from a real client. Until then, a server should accept them at any point after `SID_ENTERCHAT`.

**Brood War 1.16.1** may send `SID_STOPADV` before logon finishes. That's normal and shouldn't be treated as an error.
