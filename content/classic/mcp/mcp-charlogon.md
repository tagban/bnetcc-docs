---
title: "MCP_CHARLOGON"
layout: "packet"
protocol: "MCP"
message_id: "0x07"
categories: ["MCP", "Characters"]
products: [D2DV, D2XP]
summary: "Selects a character to play."
c2s:
  fields:
    - { type: "STRING", name: "Character name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Selected.", confidence: verified }
        - { value: "0x46", meaning: "No such character. The client returns to character select and keeps the realm connection.", confidence: verified }
        - { value: "0x7A", meaning: "Logon failed.", confidence: single }
        - { value: "0x7B", meaning: "Character has expired.", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

Selecting a *Lord of Destruction* character from a classic *Diablo II* client got players banned from official Battle.net, so a realm should refuse it instead of accepting it.
