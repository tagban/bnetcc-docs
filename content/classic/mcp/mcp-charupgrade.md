---
title: "MCP_CHARUPGRADE"
layout: "packet"
protocol: "MCP"
message_id: "0x18"
categories: ["MCP", "Characters"]
products: [D2XP]
summary: "Converts a classic character into a *Lord of Destruction* character."
c2s:
  fields:
    - { type: "STRING", name: "Character name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Upgraded.", confidence: verified }
        - { value: "0x46", meaning: "No such character.", confidence: verified }
        - { value: "0x7A", meaning: "Upgrade failed.", confidence: verified }
        - { value: "0x7B", meaning: "Character has expired.", confidence: single }
        - { value: "0x7C", meaning: "Already a *Lord of Destruction* character.", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

The upgrade can't be undone. Only a *Lord of Destruction* client can send it.
