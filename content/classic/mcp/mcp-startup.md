---
title: "MCP_STARTUP"
layout: "packet"
protocol: "MCP"
message_id: "0x01"
categories: ["MCP", "Logon"]
products: [D2DV, D2XP]
summary: "The first message on the realm connection. Hands the realm the logon data Battle.net issued, so it knows who the client is."
c2s:
  when: "Right after the `0x01` protocol byte on the realm connection."
  fields:
    - { type: "UINT32", name: "Cookie", notes: "Copied from the `SID_LOGONREALMEX` reply.", confidence: verified }
    - { type: "UINT32", name: "Status", notes: "Copied from the `SID_LOGONREALMEX` reply.", confidence: verified }
    - { type: "UINT32 × 2", name: "Chunk 1", notes: "Copied from the `SID_LOGONREALMEX` reply.", confidence: verified }
    - { type: "UINT32 × 12", name: "Chunk 2", notes: "Copied from the `SID_LOGONREALMEX` reply.", confidence: verified }
    - { type: "STRING", name: "Unique name", notes: "The account's name on Battle.net.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Accepted. The client asks for its character list next.", confidence: verified }
        - { value: "0x02, 0x0A – 0x0D", meaning: "Realm unavailable: the realm doesn't recognise the logon.", confidence: verified }
        - { value: "0x7E", meaning: "CD key banned from realm play.", confidence: single }
        - { value: "0x7F", meaning: "The address is temporarily banned from the realm.", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

The client doesn't interpret the sixteen 32-bit values. It copies them exactly as `SID_LOGONREALMEX` delivered them, so a realm that shares a process with the Battle.net server can use them to carry any handle it likes.
