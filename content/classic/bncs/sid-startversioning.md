---
title: "SID_STARTVERSIONING"
layout: "packet"
protocol: "BNCS"
message_id: "0x06"
categories: ["BNCS", "Logon", "Version checking"]
products: [SSHR, JSTR, DRTL, DSHR, W2BN]
status: "Historical. Newer games use `SID_AUTH_INFO` for the same job."
summary: "Starts the version check in the older logon: the client names its game, and the server says which check to run."
c2s:
  fields:
    - { type: "DWORD", name: "Platform code", notes: "`IX86` for Windows, sent backwards as `68XI`. See [game and platform codes](/classic/connecting/#game-and-platform-codes).", confidence: verified }
    - { type: "DWORD", name: "Product code", notes: "For example `DRTL` or `W2BN`, sent backwards: `LTRD`, `NB2W`.", confidence: verified }
    - { type: "UINT32", name: "Version byte", confidence: verified }
    - { type: "UINT32", name: "Unused", notes: "`0`.", confidence: verified }
s2c:
  when: "After `SID_CLIENTID`, the logon challenge and `SID_PING`."
  fields:
    - { type: "FILETIME", name: "Version-check file time", confidence: verified }
    - { type: "STRING", name: "Version-check file name", notes: "The MPQ that holds the version-check code.", confidence: verified }
    - { type: "STRING", name: "Version-check formula", notes: "Run over the game files to produce the EXE hash sent in `SID_REPORTVERSION`.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "older logon tested with a real Warcraft II client"
---

**UDP test.** After this reply the server sends `PKT_SERVERPING` over UDP to the client's port 6112. A real *Warcraft II* client keeps **Create** and **Join** disabled until that arrives, then confirms with `SID_UDPPINGRESPONSE` over TCP.
