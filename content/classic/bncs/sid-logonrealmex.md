---
title: "SID_LOGONREALMEX"
layout: "packet"
protocol: "BNCS"
message_id: "0x3E"
categories: ["BNCS", "Diablo II realm"]
products: [D2DV, D2XP]
summary: "Logs on to a *Diablo II* realm. The reply tells the client where the realm is and what to show it."
c2s:
  fields:
    - { type: "UINT32", name: "Client token", confidence: verified }
    - { type: "VOID", name: "Realm password proof (20 bytes)", notes: "The official client always uses the password `password`, hashed like an account logon, so it proves nothing.", confidence: verified }
    - { type: "STRING", name: "Realm name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Cookie", notes: "Echoes the client token.", confidence: verified }
    - { type: "UINT32", name: "Status", notes: "`0` on success.", confidence: verified }
    - { type: "UINT32 × 2", name: "Chunk 1", notes: "Opaque to the client; it passes them on to the realm.", confidence: verified }
    - { type: "UINT8 × 4", name: "Realm IP address", notes: "Network byte order.", confidence: verified }
    - { type: "UINT16", name: "Realm port", notes: "**Big-endian**, followed by two zero bytes. Not a 32-bit value.", confidence: verified }
    - { type: "UINT16", name: "Unused", notes: "`0`.", confidence: verified }
    - { type: "UINT32 × 12", name: "Chunk 2", notes: "Opaque to the client; it passes them on to the realm.", confidence: verified }
    - { type: "STRING", name: "Unique name", confidence: verified }
  values:
    - name: "Failure"
      items:
        - { value: "8 bytes or fewer", meaning: "Any reply this short is a failure: just the cookie and a status such as `0x80000001`, realm unavailable.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

The client copies the cookie, status and both chunks into `MCP_STARTUP` on the realm connection, so the realm can recognise the logon. BNETDocs also records a different reply layout seen from official servers around version 1.14d. The layout above is the one a real 1.14d client accepts.
