---
title: "SID_GETFILETIME"
layout: "packet"
protocol: "BNCS"
message_id: "0x33"
categories: ["BNCS", "Files"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Asks when a server file last changed, so the client knows whether to download it again."
c2s:
  fields:
    - { type: "UINT32", name: "Request ID", notes: "Chosen by the client and echoed back.", confidence: verified }
    - { type: "UINT32", name: "Unused", notes: "Echoed back.", confidence: verified }
    - { type: "STRING", name: "File name", notes: "Such as `tos_USA.txt`, `bnserver.ini` or an icons file.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Request ID", confidence: verified }
    - { type: "UINT32", name: "Unused", confidence: verified }
    - { type: "FILETIME", name: "Last changed", notes: "`0` if the server doesn't have the file.", confidence: verified }
    - { type: "STRING", name: "File name", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---

**Clients wait for this reply,** so a server must always answer, even for files it doesn't have. After the reply, the client downloads anything newer over BNFTP.

**Diablo II needs `tos-unicode_USA.txt`.** Without that file, a real *Diablo II* client disconnects when the player opens **Create Account**.
