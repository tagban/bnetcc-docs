---
title: "MCP_CHARRANK"
layout: "packet"
protocol: "MCP"
message_id: "0x16"
categories: ["MCP", "Ladder"]
products: [D2DV, D2XP]
summary: "Looks up where a character stands on the overall ladder."
c2s:
  fields:
    - { type: "UINT32", name: "Hardcore", notes: "`1` or `0`.", confidence: single }
    - { type: "UINT32", name: "Expansion", notes: "`1` or `0`.", confidence: single }
    - { type: "STRING", name: "Character name", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

BNETDocs records the server answering with `MCP_REQUESTLADDERDATA` for the page of the ladder that contains the character. Command Center found no reply handler for it in the 1.14d client and doesn't answer. Treat the reply as unresolved.
